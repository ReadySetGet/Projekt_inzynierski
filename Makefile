.PHONY: start lint lint-fix format format-check test test-watch test-coverage type-check prepare release debug

VENV_PY = .venv/Scripts/python.exe

start:
	python main.py

debug:
	PYTHONDEBUG=1 python main.py

lint:
	$(VENV_PY) -m flake8 app

lint-fix:
	$(VENV_PY) -m isort app && $(VENV_PY) -m black app

format:
	$(VENV_PY) -m black app

format-check:
	$(VENV_PY) -m black --check app

test:
	$(VENV_PY) -m pytest

test-watch:
	pytest --maxfail=1 --disable-warnings --tb=short -v

test-coverage:
	pytest --cov=app

type-check:
	$(VENV_PY) -m mypy app

prepare:
	echo "No direct husky equivalent in Python, but you can use pre-commit."

release:
	echo "Release process is project-specific." 