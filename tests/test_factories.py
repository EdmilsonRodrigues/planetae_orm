import pytest

from src.planetae_orm.models.client import Client
from src.planetae_orm.models.clients.mariadb import (
    AsyncIOMariaDBClient,
    AsyncIOMySQLClient,
)


@pytest.mark.parametrize(
    'client_tuple',
    [
        ('mysql', AsyncIOMySQLClient),
        ('mariadb', AsyncIOMariaDBClient),
        # ("postgresql", AsyncIOPostgreSQLClient),
        # ("mssql", AsyncIOMSSQLClient),
        # ("sqlite3", AsyncIOSQLite3Client),
        # ("mongodb", AsyncIOMongoDBClient),
    ],
)
def test_client_factory_mysql(client_tuple):
    client_name, client_type = client_tuple
    client = Client(client_name)
    print(client)
    assert client == client_type
