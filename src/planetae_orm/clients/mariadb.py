class MariaDBClient(SQLClient):
    cursor: aiomysql.Cursor
    connection: aiomysql.Connection

    def __init__(
        self,
        username: str,
        password: str,
        host: str,
        port: int,
        logger_file: str | None = None,
    ):
        super().__init__(
            username=username,
            password=password,
            host=host,
            port=port,
            logger_file=logger_file,
        )
        self.connection = None  # type: ignore
        self.cursor = None  # type: ignore
        self._sync_connection = mysql.connector.connect(
            user=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
        )
        self._sync_cursor = self._sync_connection.cursor()

    async def _create_connection(self) -> aiomysql.Connection:
        if self.connection is not None:
            return self.connection
        assert (
            self.username is not None
            and self.password is not None
            and self.host is not None
            and self.port is not None
        )
        return await aiomysql.connect(
            user=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
        )

    async def _execute(
        self, query: str, values: tuple | None = None, log: Any = None
    ) -> bool:
        self.connection = await self._create_connection()
        if log and self._logger:
            self._logger.info(log)
        try:
            async with self.connection.cursor() as cursor:
                if values:
                    await cursor.execute(query, values)
                else:
                    await cursor.execute(query)
            return True
        except Exception as e:
            if self._logger:
                self._logger.debug(str(e))
            raise

    async def _fetchone(
        self, query: str, values: tuple | None = None, log: Any = None
    ) -> tuple:
        self.connection = await self._create_connection()
        if log and self._logger:
            self._logger.info(log)
        try:
            async with self.connection.cursor() as cursor:
                if values:
                    await cursor.execute(query, values)
                else:
                    await cursor.execute(query)
                return await cursor.fetchone()
        except Exception as e:
            if self._logger:
                self._logger.debug(str(e))
            raise

    async def _fetchall(
        self, query: str, values: tuple | None = None, log: Any = None
    ) -> list[tuple]:
        self.connection = await self._create_connection()
        if log and self._logger:
            self._logger.info(log)
        try:
            async with self.connection.cursor() as cursor:
                if values:
                    await cursor.execute(query, values)
                else:
                    await cursor.execute(query)
                return await cursor.fetchall()
        except Exception as e:
            if self._logger:
                self._logger.debug(str(e))
            raise

    async def close(self):
        if self.connection is None:
            return True
        await self.connection.ensure_closed()
        self.connection = None  # type: ignore
        return True


class MySQLClient(MariaDBClient):
    pass


