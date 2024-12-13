import subprocess


def build():
    subprocess.run(
        ['sphinx-build', '-M', 'html', 'docs/source', 'docs/build'],
        check=False,
    )


if __name__ == '__main__':
    build()
