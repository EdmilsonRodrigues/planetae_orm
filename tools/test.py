import subprocess

markers = [
    # "mariadb",
    # "mysql",
    # "postgresql",
    # "mssql",
    'sqlite3',
    # "mongodb",
]  # Corrected spelling


def test():
    subprocess.run(
        [
            'pytest',
            '-vvv',
            '--cov=src/planetae_orm',
            '--cov-report=term-missing',
        ],
        check=False,
    )
    subprocess.run(['coverage', 'html'], check=False)


if __name__ == '__main__':
    test()
