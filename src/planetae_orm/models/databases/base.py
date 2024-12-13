class Database:
    cursor: Any
    connection: Any
    name: str
    host: str | None = None
    port: int | None = None
    username: str | None = None
    password: str | None = None
    connection_string: str | None = None
    logger_file: str | None = None

    def __init__(
        self,
        name: str,
        host: str | None = None,
        port: int | None = None,
        username: str | None = None,
        password: str | None = None,
        connection_string: str | None = None,
        logger_file: str | None = None,
    ):
        self._databases = None
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection_string = connection_string
        self.logger_file = logger_file
        if logger_file:
            self._logger = Logger('Client', log_file=logger_file)
        self.name = name

    @staticmethod
    def _get_items_from_signature(
        signature: dict,
    ) -> Generator[tuple[str, str]]:
        for key, value in signature.items():
            yield key, value

    @staticmethod
    def not_implemented(default: Any = False):
        src.logger.log_exception(NotImplementedError)
        return default

    async def initialize(self):
        return self.not_implemented(None)

    async def get_all_tables(self) -> tuple[str]:
        return self.not_implemented(None)

    async def create_table(self, table_name: str, signature: dict) -> bool:
        return self.not_implemented()

    async def get_table_description(self, table_name: str) -> dict[str, str]:
        return self.not_implemented()

    async def add_column_to_table(
        self,
        table_name: str,
        signature: dict,
        after: str | None = None,
        default: str | None = None,
        first: bool = False,
    ) -> bool:
        return self.not_implemented()

    async def add_primary_key(self, table_name: str, key: str) -> bool:
        return self.not_implemented()

    async def remove_column_from_table(
        self, table_name: str, key: str
    ) -> bool:
        return self.not_implemented()

    async def change_signature_from_column(
        self, table_name: str, signature: dict
    ) -> bool:
        return self.not_implemented()

    async def rename_column(
        self, table_name: str, old_name: str, signature: dict
    ) -> bool:
        return self.not_implemented()

    async def rename_table(
        self, old_table_name: str, new_table_name: str
    ) -> bool:
        return self.not_implemented()

    async def delete_table(self, table_name: str) -> Any:
        return self.not_implemented()

    async def truncate_table(self, table_name: str) -> bool:
        return self.not_implemented()

    async def insert_document(
        self,
        table_name: str,
        document: dict[str, Any],
        return_query: bool = False,
    ) -> bool | tuple[str, tuple]:
        return self.not_implemented()

    async def update_document(
        self, table_name: str, query: dict[str, Any], changes: dict[str, Any]
    ) -> bool:
        return self.not_implemented()

    async def delete_document(
        self, table_name: str, query: dict[str, Any]
    ) -> bool:
        return self.not_implemented()

    async def create_index(self, table_name: str, key: str) -> bool:
        return self.not_implemented()

    async def get_document(
        self, table_name: str, query: dict[str, Any]
    ) -> dict[str, Any] | None:
        return self.not_implemented(None)

    async def get_documents(
        self, table_name: str, query: dict[str, Any]
    ) -> list[dict[str, Any]]:  # type: ignore
        return self.not_implemented([])

    async def get_all_documents(self, table_name: str) -> list[dict[str, Any]]:
        return self.not_implemented([])

    async def backup_database(
        self, path: str, structure_only: bool = False, data_only: bool = False
    ) -> bool:
        return self.not_implemented()

    async def restore_backup(self, path: str) -> bool:
        return self.not_implemented()

    async def delete_database(self) -> bool:
        return self.not_implemented()
