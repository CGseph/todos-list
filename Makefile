.PHONY: load-initial-data migrate up create-migrations run-database


MIGRATION_MESSAGE ?= "Auto-generated migration"

load-initial-data:
	PYTHONPATH=. python src/load_initial_data.py

migrate:
	alembic upgrade head

create-migrations:
	alembic revision --autogenerate -m $(MIGRATION_MESSAGE)

up:
	docker-compose up

run-database:
	docker-compose up postgres

setup: migrate load-initial-data