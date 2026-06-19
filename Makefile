.PHONY: dev test lint up down migrate

dev:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	cd backend && python -m pytest tests/ -v

lint:
	cd backend && python -m ruff check app/
	cd backend && python -m ruff format --check app/

format:
	cd backend && python -m ruff format app/

up:
	cd infra/docker && docker compose up -d

down:
	cd infra/docker && docker compose down

migrate:
	cd backend && alembic upgrade head

migrate-new:
	cd backend && alembic revision --autogenerate -m "$(msg)"

seed:
	cd backend && python -m scripts.seed_data
