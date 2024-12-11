class Client(ABC):
    cursor: Any
    connection: Any
    host: str | None = None
    port: int | None = None
    _databases: set[str] | None = None
    username: str | None = None
    password: str | None = None
    connection_string: str | None = None
    logger_file: str | None = None
    _automatically_create_database: bool = False

    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        username: str | None = None,
        password: str | None = None,
        connection_string: str | None = None,
        logger_file: str | None = None,
        automatically_create_database: bool = False,
    ):
        self._databases = None
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection_string = connection_string
        self.logger_file = logger_file
        if logger_file:
            self._logger = Logger("Client", log_file=logger_file)
        if automatically_create_database:
            self._automatically_create_database = True

    @property
    def automatically_create_database(self) -> bool:
        return self._automatically_create_database

    @automatically_create_database.setter
    def automatically_create_database(self, value: bool):
        self._automatically_create_database = value

    def __aiter__(self):
        return self

    async def __anext__(self) -> Database | None:
        if self._databases is None:
            self._databases = await self.get_databases_names()
        try:
            database = self._databases.pop()
            return await self.get_database(database)
        except KeyError:
            raise StopAsyncIteration

    @abstractmethod
    def __getitem__(self, item: str) -> Database:
        pass

    @abstractmethod
    async def create_database(self, name: str, exist_ok: bool = True) -> bool:
        pass

    @abstractmethod
    async def get_databases(self) -> AsyncGenerator[Database | None]:
        yield

    @abstractmethod
    async def get_databases_names(self) -> set:
        pass

    @abstractmethod
    async def get_database(self, name: str) -> Database | None:
        pass

    @abstractmethod
    async def delete_database(self, name: str) -> bool:
        pass

    @classmethod
    def _get_database_class(cls) -> type:
        from importlib import import_module

        def get_database_class_name(cls):
            return cls.__name__.replace("Client", "Database")

        return getattr(
            import_module("src.planetae_db.database"),
            get_database_class_name(cls=cls),
        )

    async def close(self):
        if self.connection is None:
            return True
        self.connection.close()
        self.connection = None
        return True


