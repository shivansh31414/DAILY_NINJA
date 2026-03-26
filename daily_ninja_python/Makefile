.PHONY: help install install-dev test lint format migrate run-backend run-frontend run-celery docker-build docker-up docker-down run-azure docker-build-azure docker-push-azure azure-help azure-acr-setup azure-build-push azure-deploy azure-autoscale azure-verify

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

run-azure: ## Run backend with Gunicorn for Azure
	gunicorn backend.run:app --bind 0.0.0.0:8000 --workers 4

docker-build: ## Build Docker images
	docker-compose -f docker/docker-compose.yml build

docker-build-azure: ## Build Docker image for Azure
	docker build -f docker/Dockerfile.azure -t daily-ninja:azure .

docker-push-azure: ## Push Docker image to Azure
	docker push daily-ninja:azure

azure-help: ## Show Azure deployment instructions
	@cat ../docs/AZURE_DEPLOY.md

azure-acr-setup: ## Create Azure resource group and ACR
	bash ../scripts/azure/01_setup_rg_acr.sh

azure-build-push: ## Build and push image to ACR
	bash ../scripts/azure/02_build_push.sh

azure-deploy: ## Deploy container to Azure Web App
	bash ../scripts/azure/03_deploy_webapp.sh

azure-autoscale: ## Configure autoscaling for App Service Plan
	bash ../scripts/azure/05_configure_autoscale.sh

azure-verify: ## Verify deployed app and run post-deploy integration checks
	bash ../scripts/azure/04_verify_deployment.sh
