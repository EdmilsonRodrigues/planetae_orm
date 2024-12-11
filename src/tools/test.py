import subprocess
import sys

markers = [
    "mariadb",
    "mysql",
    "postgresql",
    "mssql",
    "sqlite3",
    "mongodb",
]  # Corrected spelling


def test():
    subprocess.run("tox")


if __name__ == "__main__":
    test()
