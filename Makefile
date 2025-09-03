.PHONY: load-initial-data migrate up create-migrations start-database build help initial-setup stop-database


MIGRATION_MESSAGE ?= "Auto-generated migration"

help:
	@echo "Available commands:"
	@echo "  make migrate        		- Apply alembic migrations in DB"
	@echo "  make create-migrations 	- Create alembic migration files"
	@echo "  make load-initial-data 	- Create initial superuser in DB"
	@echo "  make up 					- Full start the application + DB"
	@echo "  make run-database 			- Start database service"
	@echo "  make initial-setup			- Configurate initial setup for services"
	@echo "  make build					- Build images"


load-initial-data:
	PYTHONPATH=. python src/load_initial_data.py

migrate:
	alembic upgrade head

create-migrations:
	alembic revision --autogenerate -m $(MIGRATION_MESSAGE)

up:
	docker-compose up

start-database:
	@echo "Running database in background"
	docker-compose up -d postgres

stop-database:
	@echo "Stopping database."
	docker-compose down

build:
	docker-compose build

initial-setup: start-database migrate load-initial-data stop-database
	@echo "Startup completed"
