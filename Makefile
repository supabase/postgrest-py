install:
	poetry install

install_poetry:
	curl -sSL https://install.python-poetry.org | python -

tests: install tests_only tests_pre_commit

tests_pre_commit:
	poetry run pre-commit run --all-files

tests_only:
	poetry run pytest --cov=./ --cov-report=xml -vv

run_infra:
	cd infra &&\
	docker-compose down &&\
	docker-compose up -d

clean_infra:
	cd infra &&\
	docker-compose down --remove-orphans &&\
	docker system prune -a --volumes -f

run_tests: tests

build_sync:
	poetry run unasync postgrest_py tests
