import asyncio
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from typing import Any, Self

from models.database import Database
from models.exceptions import ClientException
from models.meta import AbstractMetaSingleton


class AsyncIOPlanetaeClient[D: Database](ABC, metaclass=AbstractMetaSingleton):
    """Base class for all clients."""

    host: str | None = None
    port: int | None = None
    _automatically_create_database: bool = False
    _connection: Any
    _cursor: Any
    _databases: set[str]
    _iterating: bool = False

    @abstractmethod
    async def execute(self, query: str, values: tuple | None = None) -> bool:
        pass

    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        automatically_create_database: bool = False,
    ):
        self.host = host
        self.port = port
        self._automatically_create_database = automatically_create_database
        self.__startup()
        self._iterating = False

    def __startup(self):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.run_until_complete(self.__async_startup())

    async def __async_startup(self):
        self._databases = await self.get_databases_names()

    @property
    def automatically_create_database(self) -> bool:
        return self._automatically_create_database

    def __aiter__(self):
        return self

    async def __anext__(self) -> D | None:
        if not self._iterating:
            self._iterating = True
        try:
            database = self._databases.pop()
            return await self.get_database(database)
        except KeyError:
            self._databases = await self.get_databases_names()
            self._iterating = False
            raise StopAsyncIteration

    @abstractmethod
    def __getitem__(self, item: str) -> D:
        if item in self._databases:
            loop = asyncio.get_running_loop()
            db = loop.run_until_complete(self.get_database(item))
            if db is None:
                raise ClientException(f'Database {item} does not exist.')
            return db
        if self._automatically_create_database:
            loop = asyncio.get_running_loop()
            created = loop.run_until_complete(self.create_database(item))
            if not created:
                raise ClientException(f'Database {item} could not be created.')
            return self[item]
        raise ClientException(f'Database {item} does not exist.')

    @abstractmethod
    def __getattribute__(self, name: str) -> Any:
        try:
            return super().__getattribute__(name)
        except AttributeError:
            return self[name]

    @abstractmethod
    async def create_database(self, name: str, exist_ok: bool = True) -> bool:
        """Create a database."""
        self._databases.add(name)
        pass

    @abstractmethod
    async def get_databases(self) -> AsyncGenerator[D | None]:
        yield

    @abstractmethod
    async def get_databases_names(self) -> set:
        pass

    @abstractmethod
    async def get_database(self, name: str) -> D | None:
        pass

    @abstractmethod
    def delete_database(self, name: str) -> bool:
        """Delete a database."""
        self._databases.remove(name)
        pass

    @classmethod
    def _get_database_class(cls) -> type[D]:
        from importlib import import_module

        def get_database_class_name(cls: type[Self]) -> str:
            return cls.__name__.replace('Client', 'Database')

        return getattr(
            import_module('src.planetae_db.database'),
            get_database_class_name(cls=cls),
        )

    async def close(self) -> bool:
        if self.connection is None:
            return True
        self.connection.close()
        self.connection = None
        return True
