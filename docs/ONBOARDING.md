# Developer Onboarding Guide

Welcome to ECOMMDEV! This guide gets you up and running quickly.

## Prerequisites

- Docker & Docker Compose
- Python 3.11+

## Quick Start

```bash
git clone https://github.com/kelsonbrito50/ecommdev-demo.git
cd ecommdev-demo
cp .env.example .env
docker-compose up --build
```

App available at:
- Django: http://localhost:8000
- Admin: http://localhost:8000/admin/

## Initial Setup

```bash
# In a new terminal:
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --noinput
```

## Architecture Overview

This is a 6-container Docker architecture:
1. **web** — Django app (Gunicorn)
2. **nginx** — Reverse proxy + static files
3. **db** — PostgreSQL
4. **redis** — Cache + Celery broker
5. **celery** — Async task worker
6. **celery-beat** — Scheduled tasks

## Development Tips

- Use `make dev` to start all services
- Use `make test` to run the test suite
- Use `make shell` to open Django shell
- Check `Makefile` for all available commands

## Module Overview

See [MODULES.md](./MODULES.md) for a breakdown of all 13 platform modules.
