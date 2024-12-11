from abc import abstractmethod
from typing import Any
from planetae_orm.client import Client


class SQLClient(Client):
    cursor: Any
    connection: Any
    _sync_cursor: Any

    @abstractmethod
    async def _execute(
        self, query: str, values: tuple | None = None, log: Any = None
    ) -> bool:
        return self._execute_sync(query, values, log)

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

    def _execute_sync(
        self, query: str, values: tuple | None = None, log: Any = None
    ) -> bool:
        try:
            if values:
                self._sync_cursor.execute(query, values)
            self._sync_cursor.execute(query)
            return True
        except Exception as e:
            raise

    async def create_database(self, name: str, exist_ok: bool = True) -> bool:
        try:
            return await self._execute(
                f"CREATE DATABASE {name} DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
            )
        except pymysql.ProgrammingError as e:
            if exist_ok:
                if self._logger:
                    self._logger.info(f"Database {name} already exists.")
                return False
            raise e

    def _get_credentials(self) -> dict[str, str | int | None]:
        return {
            "username": self.username,
            "password": self.password,
            "host": self.host,
            "port": self.port,
        }

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
        query = "SHOW DATABASES;"
        return set(
            tup[0]
            for tup in await self._fetchall(
                query=query, log="Fetched all the tables of database."
            )
        )

    async def delete_database(self, name: str) -> bool:
        query = f"DROP DATABASE {name};"
        return await self._execute(query, log=f"Dropped database {name}.")
