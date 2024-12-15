import asyncio

import aiomysql

from src.planetae_orm.models.databases.mariadb import (
    AsyncIOMariaDBDatabase,
    AsyncioMySQLDatabase,
)
from src.planetae_orm.models.exceptions import ClientException
from src.planetae_orm.models.clients.sql import AsyncIOSQLClient


class AsyncIOMariaDBClient[D = AsyncIOMariaDBDatabase](AsyncIOSQLClient):
    cursor: aiomysql.Cursor
    connection: aiomysql.Connection

    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
    ) -> None:
        """
        Initialize the AsyncIOMariaDBClient.

        :param host: The host of the database
        :type host: str
        :param port: The port of the database
        :type port: int
        :param username: The username to connect to the database
        :type username: str
        :param password: The password to connect to the database
        :type password: str
        """
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

    async def open(self) -> bool:
        """
        Open the connection.

        :return: True if the connection was opened successfully
        :rtype: bool
        """
        self.cursor = await self.connection.cursor()
        return True

    async def close(self) -> bool:
        """
        Close the connection.

        :return: True if the connection was closed successfully
        :rtype: bool
        """
        await self.cursor.close()
        return True

    async def create_database(self, name: str, exist_ok: bool = True) -> bool:
        """
        Create a database.

        :param name: The name of the database to create
        :type name: str
        :param exist_ok: If True, will not raise an error if the database
            already exists
        :type exist_ok: bool

        :return: True if the database was created successfully
        :rtype: bool
        """
        if_sentence = 'IF NOT EXISTS' if exist_ok else ''
        return await self.execute(
            ' '.join((
                f'CREATE DATABASE {if_sentence} {name} DEFAULT CHARACTER SET',
                'utf8mb4 COLLATE utf8mb4_unicode_ci;',
            ))
        )

    async def get_database(self, name: str) -> D:
        """
        Get a database by name.

        :param name: The name of the database to get
        :type name: str

        :return: The database if it exists
        :rtype: D
        """
        if name in self._databases:
            return D(name, self)
        if self._automatically_create_database:
            if await self.create_database(name):
                return D(name, self)
        raise ClientException('Database does not exist.')


class AsyncIOMySQLClient[D = AsyncioMySQLDatabase](AsyncIOMariaDBClient):
    pass
