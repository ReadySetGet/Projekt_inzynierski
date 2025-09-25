import re
import sys

REQUIRED_PATTERN = (
    r"^(test|add|cut|fix|bump|make|start|stop|refactor|reformat|optimise|"
    r"document|merge): .*$"
)
HELP = """
Wrong commit message format
Please use the following format:
test:      Add or update tests
add:       Add new features or files
cut:       Remove features or files
fix:       Fix a bug
bump:      Bump dependencies or versions
make:      General changes or improvements
start:     Begin a new feature or task
stop:      End or pause a feature or task
refactor:  Refactor code without changing functionality
reformat:  Reformat code (e.g., linting, style)
optimise:  Improve performance
document:  Add or update documentation
merge:     Merge branches

Example: fix: resolve navigation crash on Android
"""


def main():
    with open(sys.argv[1], encoding="utf-8") as f:
        message = f.read().strip()
    if not re.match(REQUIRED_PATTERN, message):
        print(HELP)
        sys.exit(1)


if __name__ == "__main__":
    main()
