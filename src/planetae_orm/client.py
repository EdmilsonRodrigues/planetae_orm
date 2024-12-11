from enum import Enum

from planetae_orm.clients.base import BaseClient


class PossibleClients(Enum):
    MYSQL = "mysql"
    MARIADB = "mariadb"
    POSTGRESQL = "postgresql"
    MSSQL = "mssql"
    SQLITE3 = "sqlite3"
    MONGODB = "mongodb"


class Client[C: BaseClient]:
    def __new__(cls, name: str | PossibleClients) -> C:
        if isinstance(name, str):
            name = PossibleClients(name.lower())
        match name:
            case PossibleClients.MYSQL:
                from planetae_orm.clients.mariadb import MySQLClient

                return MySQLClient
            case PossibleClients.MARIADB:
                from planetae_orm.clients.mariadb import MariaDBClient

                return MariaDBClient
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
                raise ValueError(f"Client {name} not supported")