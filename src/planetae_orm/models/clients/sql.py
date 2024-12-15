from abc import abstractmethod
from collections.abc import AsyncGenerator

from src.planetae_orm.models.clients.base import AsyncIOPlanetaeClient
from src.planetae_orm.models.databases.sql import AsyncIOSQLDatabase


class AsyncIOSQLClient[D: AsyncIOSQLDatabase](AsyncIOPlanetaeClient):
    async def execute(self, query: str, values: tuple | None = None) -> bool:
        async with self:
            if values:
                await self.cursor.execute(query, values)
            else:
                await self.cursor.execute(query)
        return True

    @abstractmethod
    async def fetchone(self, query: str, values: tuple | None = None) -> tuple:
        pass

    @abstractmethod
    async def fetchall(
        self, query: str, values: tuple | None = None
    ) -> list[tuple]:
        pass

    async def get_databases(self) -> AsyncGenerator[D | None]:
        for database in await self.get_databases_names():
            yield await self.get_database(database)

    async def get_databases_names(self) -> set:
        query = 'SHOW DATABASES;'
        return set(tup[0] for tup in await self.fetchall(query=query))

    async def delete_database(self, name: str) -> bool:
        query = f'DROP DATABASE {name};'
        return await self.execute(query)
