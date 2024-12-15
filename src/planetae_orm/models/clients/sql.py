from collections.abc import AsyncGenerator

from src.planetae_orm.models.clients.base import AsyncIOPlanetaeClient
from src.planetae_orm.models.databases.sql import AsyncIOSQLDatabase


class AsyncIOSQLClient[D = AsyncIOSQLDatabase](AsyncIOPlanetaeClient):
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
        async with self:
            if values:
                await self.cursor.execute(query, values)
            else:
                await self.cursor.execute(query)
        return True

    async def fetchone(self, query: str, values: tuple | None = None) -> tuple:
        """
        Fetch one row from the database.

        :param query: The query to execute
        :type query: str
        :param values: The values to pass to the query
        :type values: tuple

        :return: The row fetched
        :rtype: tuple
        """
        async with self:
            await self.cursor.execute(query, values)
            return await self.cursor.fetchone()

    async def fetchall(
        self, query: str, values: tuple | None = None
    ) -> list[tuple]:
        """
        Fetch all rows from the database.

        :param query: The query to execute
        :type query: str
        :param values: The values to pass to the query
        :type values: tuple

        :return: The rows fetched
        :rtype: list[tuple]
        """
        async with self:
            await self.cursor.execute(query, values)
            return await self.cursor.fetchall()

    async def get_databases(self) -> AsyncGenerator[D | None]:
        """
        Get all databases.

        :return: A generator of databases
        :rtype: AsyncGenerator[D | None]
        """
        for database in await self.get_databases_names():
            yield await self.get_database(database)

    async def get_databases_names(self) -> set:
        """
        Get all databases names.

        :return: A set of databases names
        :rtype: set
        """
        query = 'SHOW DATABASES;'
        return set(tup[0] for tup in await self.fetchall(query=query))

    async def delete_database(self, name: str) -> bool:
        """
        Delete a database.

        :param name: The name of the database to delete
        :type name: str

        :return: True if the database was deleted successfully
        :rtype: bool
        """
        query = f'DROP DATABASE {name};'
        return await self.execute(query)
