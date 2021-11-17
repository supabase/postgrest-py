install: install_poetry
	poetry install

install_poetry:
	curl -sSL https://install.python-poetry.org | python -

precommit: install
	poetry run pre-commit run --all-files

tests: install
	poetry run pytest --cov=./ --cov-report=xml -vv

build: install
	poetry run unasync postgrest_py tests

clean:
	sudo rm -r .venv
