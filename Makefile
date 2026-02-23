.PHONY: help install dev test lint format migrate shell clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements.txt

dev: ## Start development server
	docker-compose up

test: ## Run tests
	pytest

lint: ## Run linters
	flake8 .

format: ## Format code
	black . && isort .

migrate: ## Run migrations
	python manage.py migrate

shell: ## Open Django shell
	python manage.py shell

clean: ## Remove cache files
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null; true
	find . -name "*.pyc" -delete

collectstatic: ## Collect static files
	python manage.py collectstatic --noinput
