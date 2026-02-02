.PHONY: help install install-dev test lint format migrate run-backend run-frontend run-celery docker-build docker-up docker-down

help:
	@echo "Daily Ninja - Development Commands"
	@echo "===================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	pip install -r requirements/prod.txt

install-dev: ## Install development dependencies
	pip install -r requirements/dev.txt

test: ## Run all tests
	pytest tests/ -v --cov=backend --cov=workers

test-unit: ## Run unit tests only
	pytest tests/unit -v

test-integration: ## Run integration tests only
	pytest tests/integration -v

lint: ## Run linting checks
	black --check backend/ workers/ frontend/ tests/
	flake8 backend/ workers/ frontend/ tests/
	mypy backend/ workers/

format: ## Format code with Black
	black backend/ workers/ frontend/ tests/
	isort backend/ workers/ frontend/ tests/

migrate: ## Run database migrations
	alembic upgrade head

migrate-create: ## Create a new migration
	alembic revision --autogenerate -m "migration_name"

run-backend: ## Run FastAPI backend
	uvicorn backend.app.main:app --reload

run-frontend: ## Run Streamlit frontend
	streamlit run frontend/app.py

run-celery: ## Run Celery worker
	celery -A workers.celery_app worker --loglevel=info

run-scheduler: ## Run APScheduler
	python -m workers.schedulers.main

docker-build: ## Build Docker images
	docker-compose -f docker/docker-compose.yml build

docker-up: ## Start Docker services
	docker-compose -f docker/docker-compose.yml up -d

docker-down: ## Stop Docker services
	docker-compose -f docker/docker-compose.yml down

docker-logs: ## View Docker logs
	docker-compose -f docker/docker-compose.yml logs -f

docker-clean: ## Remove Docker containers and volumes
	docker-compose -f docker/docker-compose.yml down -v

clean: ## Clean up cache and build artifacts
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov dist build *.egg-info
