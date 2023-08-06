
import asyncio
from contextlib import ExitStack
import contextvars
from functools import partial
import io
from pathlib import Path
import typing as T
import zipfile

from aiohttp import ClientSession, TCPConnector, TraceConfig
from send2trash import send2trash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm

from .config import Config
from . import exceptions as E
from .models import ModelBase, Pkg, PkgFolder
from .resolvers import CurseResolver, WowiResolver, TukuiResolver


_UA_STRING = 'instawow (https://github.com/layday/instawow)'


def init_loop():
    "Get a loop running."
    try:
        import uvloop
    except ImportError:
        return asyncio.get_event_loop()
    else:
        return uvloop.new_event_loop()


async def _init_client(*, loop, **kwargs):
    return ClientSession(loop=loop,
                         connector=TCPConnector(loop=loop, limit_per_host=10),
                         headers={'User-Agent': _UA_STRING},
                         **kwargs)


class PkgArchive:

    __slots__ = ('archive', 'root_folders')

    def __init__(self, payload: bytes) -> None:
        self.archive = zipfile.ZipFile(io.BytesIO(payload))

        folders = sorted({Path(p).parts[0] for p in self.archive.namelist()})
        folders = [Path(p) for p in folders]
        self.root_folders = folders

    def extract(self, parent_folder: Path, *,
                overwrite: bool=False) -> None:
        "Extract the archive contents under ``parent_folder``."
        if not overwrite:
            conflicts = {f.name for f in self.root_folders} & \
                        {f.name for f in parent_folder.iterdir()}
            if conflicts:
                raise E.PkgConflictsWithPreexisting(conflicts)
        self.archive.extractall(parent_folder)


class MemberDict(dict):

    def __missing__(self, key):
        raise E.PkgOriginInvalid(origin=key)


_client = contextvars.ContextVar('_client')


class Manager:

    from .exceptions import (ManagerResult,
                             PkgInstalled, PkgUpdated, PkgRemoved,
                             ManagerError,
                             PkgAlreadyInstalled, PkgConflictsWithInstalled,
                             PkgConflictsWithPreexisting, PkgNonexistent,
                             PkgNotInstalled, PkgOriginInvalid, PkgUpToDate,
                             InternalError)

    def __init__(self, *,
                 config: Config, loop: asyncio.AbstractEventLoop=None,
                 client_factory: T.Callable=None) -> None:
        self.config = config
        self.loop = loop or init_loop()
        self.client_factory = partial(client_factory or _init_client,
                                      loop=self.loop)
        self.client = _client
        self.resolvers = MemberDict((r.origin, r(manager=self))
                                    for r in (CurseResolver, WowiResolver, TukuiResolver))

        engine = create_engine(f'sqlite:///{config.config_dir/config.db_name}')
        ModelBase.metadata.create_all(engine)
        self.db = sessionmaker(bind=engine)()

    def get(self, origin: str, id_or_slug: str) -> Pkg:
        "Retrieve a ``Pkg`` from the database."
        return self.db.query(Pkg)\
                      .filter(Pkg.origin == origin,
                              (Pkg.id == id_or_slug) | (Pkg.slug == id_or_slug))\
                      .first()

    async def resolve(self, origin: str, id_or_slug: str, strategy: str) -> Pkg:
        "Resolve an ID or slug into a ``Pkg``."
        return await self.resolvers[origin].resolve(id_or_slug,
                                                    strategy=strategy)

    async def to_install(self, origin: str, id_or_slug: str, strategy: str,
                         overwrite: bool) -> T.Callable[[], E.PkgInstalled]:
        "Retrieve a package to install."
        def install():
            archive = PkgArchive(payload)
            pkg.folders = [PkgFolder(path=self.config.addon_dir/f)
                           for f in archive.root_folders]

            conflicts = self.db.query(PkgFolder)\
                               .filter(PkgFolder.path.in_
                                        ([f.path for f in pkg.folders]))\
                               .first()
            if conflicts:
                raise self.PkgConflictsWithInstalled(conflicts.pkg)

            if overwrite:
                for path in (f.path for f in pkg.folders if f.path.exists()):
                    send2trash(str(path))
            archive.extract(parent_folder=self.config.addon_dir,
                            overwrite=overwrite)
            self.db.add(pkg)
            self.db.commit()
            return self.PkgInstalled(pkg)

        if self.get(origin, id_or_slug):
            raise self.PkgAlreadyInstalled
        pkg = await self.resolve(origin, id_or_slug, strategy)
        async with self.client.get()\
                              .get(pkg.download_url) as response:
            payload = await response.read()
        return install

    async def to_update(self, origin: str,
                        id_or_slug: str) -> T.Callable[[], E.PkgUpdated]:
        "Retrieve a package to update."
        def update():
            archive = PkgArchive(payload)
            new_pkg.folders = [PkgFolder(path=self.config.addon_dir/f)
                               for f in archive.root_folders]

            conflicts = self.db.query(PkgFolder)\
                               .filter(PkgFolder.path.in_
                                        ([f.path for f in new_pkg.folders]),
                                       PkgFolder.pkg_origin != new_pkg.origin,
                                       PkgFolder.pkg_id != new_pkg.id)\
                               .first()
            if conflicts:
                raise self.PkgConflictsWithInstalled(conflicts.pkg)

            with ExitStack() as stack:
                stack.callback(self.db.commit)
                for folder in old_pkg.folders:
                    send2trash(str(folder.path))
                self.db.delete(old_pkg)
                archive.extract(parent_folder=self.config.addon_dir)
                self.db.add(new_pkg)
            return self.PkgUpdated(old_pkg, new_pkg)

        old_pkg = self.get(origin, id_or_slug)
        if not old_pkg:
            raise self.PkgNotInstalled
        new_pkg = await self.resolve(origin, id_or_slug, old_pkg.options.strategy)
        if old_pkg.file_id == new_pkg.file_id:
            raise self.PkgUpToDate

        async with self.client.get()\
                              .get(new_pkg.download_url) as response:
            payload = await response.read()
        return update

    def remove(self, origin: str, id_or_slug: str) -> E.PkgRemoved:
        "Remove a package."
        pkg = self.get(origin, id_or_slug)
        if not pkg:
            raise self.PkgNotInstalled

        for folder in pkg.folders:
            send2trash(str(folder.path))
        self.db.delete(pkg)
        self.db.commit()
        return self.PkgRemoved(pkg)


Bar = partial(tqdm, leave=False, ascii=True)

_dl_counter = contextvars.ContextVar('_dl_counter', default=0)


def _post_increment_dl_counter():
    val = _dl_counter.get()
    _dl_counter.set(val + 1)
    return val


async def _init_cli_client(*, loop):
    async def do_on_request_end(session, context, params):
        if (params.response.content_length and
                # Ignore files smaller than a megabyte
                params.response.content_length > 2**20):
            filename = params.response.headers.get('Content-Disposition', '')
            filename = filename[(filename.find('"') + 1):filename.rfind('"')] or \
                       params.response.url.name
            bar = Bar(total=params.response.content_length,
                      desc=f'Downloading {filename}',
                      miniters=1, unit='B', unit_scale=True,
                      position=_post_increment_dl_counter())

            async def ticker(bar=bar, params=params):
                while True:
                    if params.response.content._cursor == bar.total:
                        bar.close()
                        break
                    bar.update(params.response.content._cursor - bar.n)
                    # The polling frequency's gotta be high
                    # (higher than the ``tqdm.mininterval`` default)
                    # so this bar gets to flush itself down the proverbial
                    # drain before ``CliManager.gather``'s bar or it's gonna
                    # leave behind an empty line which would be, truly,
                    # devastating
                    await asyncio.sleep(.01)
            loop.create_task(ticker())

    trace_conf = TraceConfig()
    trace_conf.on_request_end.append(do_on_request_end)
    trace_conf.freeze()
    return await _init_client(loop=loop, trace_configs=[trace_conf])


async def _intercept_exc_async(index, awaitable):
    try:
        result = await awaitable
    except E.ManagerError as error:
        result = error
    except Exception as error:
        result = E.InternalError(error=error)
    return index, result


def _intercept_exc(callable_):
    try:
        result = callable_()
    except E.ManagerError as error:
        result = error
    except Exception as error:
        result = E.InternalError(error=error)
    return result


class CliManager(Manager):

    def __init__(self, *,
                 config: Config, loop: asyncio.AbstractEventLoop=None,
                 show_progress: bool=True) -> None:
        super().__init__(config=config, loop=loop,
                         client_factory=_init_cli_client if show_progress else None)
        self.show_progress = show_progress

    def run(self, awaitable: T.Awaitable) -> T.Any:
        "Run ``awaitable`` inside an explicit context."
        async def runner():
            async with (await self.client_factory()) as client:
                _client.set(client)
                return await awaitable

        return contextvars.copy_context().run(partial(self.loop.run_until_complete,
                                                      runner()))

    async def gather(self, it: T.Iterable, **kwargs) -> list:
        futures = [_intercept_exc_async(*i) for i in enumerate(it)]
        results = [None] * len(futures)
        with Bar(total=len(futures), disable=not self.show_progress,
                 position=_post_increment_dl_counter(), **kwargs) as bar:
            for result in asyncio.as_completed(futures, loop=self.loop):
                results.__setitem__(*await result)
                bar.update(1)
        return results

    def resolve_many(self, values: T.Iterable) -> list:
        return self.run(self.gather((self.resolve(*a) for a in values),
                                    desc='Resolving'))

    def install_many(self, values: T.Iterable) -> list:
        result = self.run(self.gather((self.to_install(*a) for a in values),
                                      desc='Fetching'))
        return [_intercept_exc(i) for i in result]

    def update_many(self,  values: T.Iterable) -> list:
        result = self.run(self.gather((self.to_update(*a) for a in values),
                                      desc='Checking'))
        return [_intercept_exc(i) for i in result]
