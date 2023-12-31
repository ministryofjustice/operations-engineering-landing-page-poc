.ONESHELL:

PYTHON_SOURCE_FILES = ./tests operations_engineering_landing_page.py ./landing_page_app

help:
	@echo "Available commands:"
	@echo "make venv             - venv the environment"
	@echo "make test             - Run tests"
	@echo "make local            - Run application locally"
	@echo "make lint             - Run Lint tools"
	@echo "make format           - Run Code formatting tools"
	@echo "make report           - Open the Code Coverage report"

venv: requirements.txt
	python3 -m venv venv .venv
	venv/bin/pip3 install --upgrade pip
	venv/bin/pip3 install -r requirements.txt

lint: venv
	venv/bin/pip3 install flake8
	venv/bin/pip3 install mypy
	venv/bin/pip3 install pylint
	venv/bin/flake8 --ignore=E501,W503,E302 $(PYTHON_SOURCE_FILES)
	venv/bin/pylint --recursive=y $(PYTHON_SOURCE_FILES)
	venv/bin/mypy --ignore-missing-imports $(PYTHON_SOURCE_FILES)

format: venv
	venv/bin/pip3 install black
	venv/bin/black $(PYTHON_SOURCE_FILES)

test: venv
	venv/bin/pip3 install coverage
	export FLASK_CONFIGURATION=development; venv/bin/coverage run -m unittest discover

report:
	venv/bin/coverage html && open htmlcov/index.html

clean-test:
	rm -fr venv
	rm -fr .venv
	rm -fr .tox/
	rm -fr .pytest_cache
	rm -fr .mypy_cache
	rm -fr .coverage
	rm -fr htmlcov/

local: venv
	export FLASK_CONFIGURATION=development; venv/bin/python3 -m operations_engineering_landing_page

all:

.PHONY: venv lint test format local clean-test report all
