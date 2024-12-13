class MariaDBDatabase(SQLDatabase):
    def __init__(
        self,
        name: str,
        host: str,
        port: int,
        username: str,
        password: str,
        logger_file: str | None = None,
    ):
        super().__init__(
            name=name,
            host=host,
            port=port,
            username=username,
            password=password,
            logger_file=logger_file,
        )
        self.connection = mariadb.connect(
            user=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.name,
        )
        self.cursor = self.connection.cursor()


class MySQLDatabase(MariaDBDatabase):
    pass
