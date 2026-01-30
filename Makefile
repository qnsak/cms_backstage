.DEFAULT_GOAL := help

.PHONY: help up down logs shell test test-report test-report-local fmt lint db-reset seed migrate revision typecheck

help: ## 顯示可用指令
	@echo ""
	@echo "Available commands:"
	@echo "-------------------"
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) 		| awk 'BEGIN {FS = ":.*?## "}; {printf "  %-12s %s\n", $$1, $$2}'
	@echo ""

up: ## Build and start the containers
	docker compose up --build

down: ## Stop and remove containers
	docker compose down

logs: ## Follow backend logs
	docker compose logs -f

shell: ## Open a bash shell inside container
	docker compose run --rm backend bash

test: ## Run pytest (in-memory DB)
	docker compose run --rm backend pytest -q

test-report: ## Run pytest with junit/html/coverage reports
	docker compose run --rm --build backend bash -lc "mkdir -p reports && pytest -q \
		--junitxml=reports/junit.xml \
		--html=reports/pytest.html --self-contained-html \
		--cov=src/cms --cov-report=xml:reports/coverage.xml --cov-report=html:reports/coverage-html"

test-report-local: ## Run pytest reports locally (no docker)
	mkdir -p reports
	pytest -q \
		--junitxml=reports/junit.xml \
		--html=reports/pytest.html --self-contained-html \
		--cov=src/cms --cov-report=xml:reports/coverage.xml --cov-report=html:reports/coverage-html

fmt: ## Format code with ruff
	docker compose run --rm backend ruff format .

lint: ## Lint code with ruff
	docker compose run --rm backend ruff check .

db-reset: ## Reset SQLite database (DANGER: deletes app.db)
	rm -f app.db
	@echo "SQLite database reset: app.db removed"

seed: ## Seed initial demo data into SQLite
	docker compose run --rm backend python -m cms.scripts.seed

migrate: ## Run Alembic migrations
	docker compose run --rm backend alembic upgrade head

revision: ## Create new migration (autogenerate): make revision m="message"
	docker compose run --rm backend alembic revision --autogenerate -m "$(m)"
