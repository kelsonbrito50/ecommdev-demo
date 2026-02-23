# Deployment Guide

## Prerequisites

- Docker & Docker Compose
- PostgreSQL 15+

## Quick Start

```bash
cp .env.example .env
docker-compose up --build
python manage.py migrate
python manage.py createsuperuser
```

App available at http://localhost:8000

## Production

Use a production-grade WSGI server:
```bash
gunicorn core.wsgi:application --bind 0.0.0.0:8000
```
