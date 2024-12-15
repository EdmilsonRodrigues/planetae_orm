from functools import cache

from planetae_orm.models.client import SupportedClients
from src.planetae_orm.models.databases.base import AsyncIOPlanetaeDatabase


@cache
class Database[D: AsyncIOPlanetaeDatabase]:
    def __new__(cls, name: str | SupportedClients) -> D:
        if isinstance(name, str):
            name = SupportedClients(name.lower())
        match name:
            case SupportedClients.MYSQL:
                from src.planetae_orm.models.clients.mariadb import (
                    AsyncIOMySQLClient,
                )

                return AsyncIOMySQLClient
            case SupportedClients.MARIADB:
                from src.planetae_orm.models.clients.mariadb import (
                    AsyncIOMariaDBClient,
                )

                return AsyncIOMariaDBClient
            # case SupportedClients.POSTGRESQL:
            #     from planetae_orm.clients.postgresql import PostgreSQLClient
            #     return PostgreSQLClient
            # case SupportedClients.MSSQL:
            #     from planetae_orm.clients.mssql import MSSQLClient
            #     return MSSQLClient
            # case SupportedClients.SQLITE3:
            #     from planetae_orm.clients.sqlite3 import SQLite3Client
            #     return SQLite3Client
            # case SupportedClients.MONGODB:
            #     from planetae_orm.clients.mongodb import MongoDBClient
            #     return MongoDBClient
            case _:
                raise ValueError(f'Client {name} not supported')
