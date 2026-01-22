# ECOMMDEV - Makefile
# Convenience commands for development and deployment

.PHONY: help install run migrate makemigrations test lint format clean docker-build docker-up docker-down

# Default target
help:
	@echo "ECOMMDEV - Available commands:"
	@echo ""
	@echo "  Development:"
	@echo "    make install      - Install dependencies"
	@echo "    make run          - Run development server"
	@echo "    make migrate      - Run database migrations"
	@echo "    make makemigrations - Create new migrations"
	@echo "    make createsuperuser - Create admin user"
	@echo "    make shell        - Open Django shell"
	@echo "    make loaddata     - Load initial fixtures"
	@echo ""
	@echo "  Testing & Quality:"
	@echo "    make test         - Run tests"
	@echo "    make lint         - Run linter"
	@echo "    make format       - Format code"
	@echo "    make coverage     - Run tests with coverage"
	@echo ""
	@echo "  Docker:"
	@echo "    make docker-build - Build Docker images"
	@echo "    make docker-up    - Start containers"
	@echo "    make docker-down  - Stop containers"
	@echo "    make docker-dev   - Start dev environment"
	@echo "    make docker-logs  - View container logs"
	@echo ""
	@echo "  Utilities:"
	@echo "    make clean        - Clean temporary files"
	@echo "    make messages     - Generate translation files"
	@echo "    make compilemessages - Compile translation files"
	@echo "    make collectstatic - Collect static files"

# Development
install:
	pip install -r requirements.txt

run:
	python manage.py runserver

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

createsuperuser:
	python manage.py createsuperuser

shell:
	python manage.py shell

loaddata:
	python manage.py loaddata fixtures/initial_data.json

# Testing & Quality
test:
	pytest

lint:
	flake8 .

format:
	black .
	isort .

coverage:
	pytest --cov=. --cov-report=html
	@echo "Coverage report available at htmlcov/index.html"

# Docker commands
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-dev:
	docker-compose -f docker-compose.dev.yml up

docker-logs:
	docker-compose logs -f

docker-shell:
	docker-compose exec web python manage.py shell

docker-migrate:
	docker-compose exec web python manage.py migrate

# Utilities
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

messages:
	python manage.py makemessages -l pt_BR -l en

compilemessages:
	python manage.py compilemessages

collectstatic:
	python manage.py collectstatic --noinput

# Production
deploy:
	@echo "Deploying to production..."
	git pull origin main
	docker-compose build
	docker-compose up -d
	docker-compose exec web python manage.py migrate
	docker-compose exec web python manage.py collectstatic --noinput
	@echo "Deployment complete!"
