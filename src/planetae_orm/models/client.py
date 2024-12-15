from enum import Enum
from functools import cache

from src.planetae_orm.models.clients.base import AsyncIOPlanetaeClient


class PossibleClients(Enum):
    MYSQL = 'mysql'
    MARIADB = 'mariadb'
    POSTGRESQL = 'postgresql'
    MSSQL = 'mssql'
    SQLITE3 = 'sqlite3'
    MONGODB = 'mongodb'


@cache
class Client:
    def __new__(
        cls, name: str | PossibleClients
    ) -> type[AsyncIOPlanetaeClient]:
        if isinstance(name, str):
            name = PossibleClients(name.lower())
        match name:
            case PossibleClients.MYSQL:
                from src.planetae_orm.models.clients.mariadb import (
                    AsyncIOMySQLClient,
                )

                return AsyncIOMySQLClient
            case PossibleClients.MARIADB:
                from src.planetae_orm.models.clients.mariadb import (
                    AsyncIOMariaDBClient,
                )

                return AsyncIOMariaDBClient
            # case PossibleClients.POSTGRESQL:
            #     from planetae_orm.clients.postgresql import PostgreSQLClient
            #     return PostgreSQLClient
            # case PossibleClients.MSSQL:
            #     from planetae_orm.clients.mssql import MSSQLClient
            #     return MSSQLClient
            # case PossibleClients.SQLITE3:
            #     from planetae_orm.clients.sqlite3 import SQLite3Client
            #     return SQLite3Client
            # case PossibleClients.MONGODB:
            #     from planetae_orm.clients.mongodb import MongoDBClient
            #     return MongoDBClient
            case _:
                raise ValueError(f'Client {name} not supported')
