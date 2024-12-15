import asyncio
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from typing import Any, Self

from src.planetae_orm.models.databases.base import (
    AsyncIOPlanetaeDatabase,
)
from src.planetae_orm.models.exceptions import ClientException
from src.planetae_orm.models.meta import AbstractMetaSingleton


class AsyncIOPlanetaeClient[D: AsyncIOPlanetaeDatabase](
    ABC, metaclass=AbstractMetaSingleton
):
    """Base class for all clients."""

    host: str
    port: int
    _automatically_create_database: bool = False
    _databases: set[str]
    _iterating: bool = False

    @property
    def automatically_create_database(self) -> bool:
        return self._automatically_create_database

    def __init__(
        self,
        host: str,
        port: int,
        automatically_create_database: bool = True,
    ):
        self._host = host
        self._port = port
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

    async def __aenter__(self):
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

    @abstractmethod
    def __getitem__(self, item: str) -> D:
        loop = asyncio.get_running_loop()
        if item in self._databases:
            db = loop.run_until_complete(self.get_database(item))
            if db is None:
                raise ClientException(f'Database {item} does not exist.')
            return db
        if self._automatically_create_database:
            if not loop.run_until_complete(self.create_database(item)):
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
    async def execute(self, query: str, values: tuple | None = None) -> bool:
        """
        Execute a query in the database.

        :param query: The query to execute
        :type query: str
        :param values: The values to pass to the query
        :type values: tuple

        :return: True if the query was executed successfully
        :rtype: bool
        """
        pass

    @abstractmethod
    async def open(self) -> bool:
        pass

    @abstractmethod
    async def close(self) -> bool:
        pass

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
    async def delete_database(self, name: str) -> bool:
        """Delete a database."""
        self._databases.remove(name)
        pass

    @abstractmethod
    async def fetchone(self, query: str, values: tuple | None = None) -> tuple:
        pass

    @abstractmethod
    async def fetchall(
        self, query: str, values: tuple | None = None
    ) -> list[tuple]:
        pass

    @classmethod
    def _get_database_class(cls) -> type[D]:
        from importlib import import_module

        def get_database_class_name(cls: type[Self]) -> str:
            return cls.__name__.replace('Client', 'Database')

        return getattr(
            import_module(__name__.replace('clients', 'databases')),
            get_database_class_name(cls=cls),
        )
