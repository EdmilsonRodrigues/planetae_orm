import subprocess


def build():
    subprocess.run(["sphinx-build", "-M", "html", "docs/source", "docs/build"])


if __name__ == "__main__":
    build()
