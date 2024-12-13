from abc import abstractmethod
from typing import Any

from planetae_orm.models.clients.base import AsyncIOPlanetaeClient


class AsyncIOSQLClient(AsyncIOPlanetaeClient):
    def __init__(self):
        pass

    @abstractmethod
    async def _fetchone(
        self, query: str, values: tuple | None = None, log: Any = None
    ) -> tuple:
        pass

    @abstractmethod
    async def _fetchall(
        self, query: str, values: tuple | None = None, log: Any = None
    ) -> list[tuple]:
        pass

    async def create_database(self, name: str, exist_ok: bool = True) -> bool:
        try:
            return await self.execute(
                ' '.join((
                    f'CREATE DATABASE {name} DEFAULT CHARACTER SET',
                    'utf8mb4 COLLATE utf8mb4_unicode_ci;',
                ))
            )
        except Exception as e:
            self._handle_create_database_exception(e, exist_ok)

    @abstractmethod
    def _handle_create_database_exception(
        self, exception: Exception, exist_ok: bool
    ):
        if not exist_ok:
            raise exception

    async def get_database(self, name: str):
        try:
            database = self._get_database_class()
            return database(**self._get_credentials(), name=name)
        except mariadb.ProgrammingError:
            if self.automatically_create_database:
                await self.create_database(name)
                return await self.get_database(name)
            raise

    async def get_databases(self) -> AsyncGenerator[Database | None]:
        databases = await self.get_databases_names()
        for database in databases:
            yield await self.get_database(database)

    async def get_databases_names(self) -> set:
        query = 'SHOW DATABASES;'
        return set(
            tup[0]
            for tup in await self._fetchall(
                query=query, log='Fetched all the tables of database.'
            )
        )

    async def delete_database(self, name: str) -> bool:
        query = f'DROP DATABASE {name};'
        return await self._execute(query, log=f'Dropped database {name}.')
