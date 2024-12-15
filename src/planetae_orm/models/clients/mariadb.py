import asyncio

import aiomysql

from planetae_orm.models.databases.mariadb import AsyncIOMariaDBDatabase
from src.planetae_orm.models.clients.sql import AsyncIOSQLClient


class AsyncIOMariaDBClient[D: AsyncIOMariaDBDatabase](AsyncIOSQLClient):
    cursor: aiomysql.Cursor
    connection: aiomysql.Connection

    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
    ):
        super().__init__(
            host=host,
            port=port,
        )
        self._username = username
        self._password = password
        loop = asyncio.get_running_loop()
        self.connection = loop.run_until_complete(
            aiomysql.connect(
                host=self._host,
                port=self._port,
                user=self._username,
                password=self._password,
            )
        )

    async def open(self):
        self.cursor = await self.connection.cursor()
        return True

    async def close(self):
        await self.cursor.close()
        return True

    async def fetchone(self, query: str, values: tuple | None = None) -> tuple:
        async with self:
            await self.cursor.execute(query, values)
            return await self.cursor.fetchone()

    async def fetchall(
        self, query: str, values: tuple | None = None
    ) -> list[tuple]:
        async with self:
            await self.cursor.execute(query, values)
            return await self.cursor.fetchall()

    async def create_database(self, name: str, exist_ok: bool = True) -> bool:
        if_sentence = 'IF NOT EXISTS' if exist_ok else ''
        return await self.execute(
            ' '.join((
                f'CREATE DATABASE {if_sentence} {name} DEFAULT CHARACTER SET',
                'utf8mb4 COLLATE utf8mb4_unicode_ci;',
            ))
        )

    async def get_database(self, name: str) -> D | None:
        return await super().get_database(name)


class MySQLClient(AsyncIOMariaDBClient):
    pass
