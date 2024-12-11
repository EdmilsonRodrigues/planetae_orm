import subprocess


def lint_and_format():
    try:
        subprocess.run(["ruff", "check", "--fix"])
        subprocess.run(["ruff", "format", "--preview"])
        subprocess.run(["mypy", "."])

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    lint_and_format()
