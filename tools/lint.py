import subprocess


def lint_and_format():
    try:
        subprocess.run(['ruff', 'check', '--fix'], check=False)
        subprocess.run(['ruff', 'format', '--preview'], check=False)
        subprocess.run(['mypy', '.'], check=False)

    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    lint_and_format()
