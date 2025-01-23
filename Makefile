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
	docker compose down &&\
	docker compose up -d

clean_infra:
	cd infra &&\
	docker compose down --remove-orphans &&\
	docker system prune -a --volumes -f

stop_infra:
	cd infra &&\
	docker compose down --remove-orphans

run_tests: run_infra sleep tests

run_unasync:
	poetry run unasync postgrest tests

build_sync: run_unasync remove_pytest_asyncio_from_sync

remove_pytest_asyncio_from_sync:
	sed -i 's/@pytest.mark.asyncio//g' tests/_sync/test_client.py
	sed -i 's/_async/_sync/g' tests/_sync/test_client.py
	sed -i 's/Async/Sync/g' tests/_sync/test_client.py

sleep:
	sleep 2
