.PHONY: install run test lint format clean freeze

PYTHON := .venv/bin/python

install:
	$(PYTHON) -m pip install -r requirements.txt

dev:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) -m app.main

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check app tests

format:
	$(PYTHON) -m ruff format app tests

freeze:
	$(PYTHON) -m pip freeze > requirements.txt

clean:
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete