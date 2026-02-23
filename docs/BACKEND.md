# Backend Development Guide

## Stack

- **Framework:** Django 4.2
- **Database:** PostgreSQL 15
- **Cache:** Redis 7
- **Task Queue:** Celery + Redis broker
- **Storage:** AWS S3 (production) / local (dev)

## App Structure

```
apps/
├── core/         # Shared utilities, base models
├── products/     # Product catalog, categories, variants
├── orders/       # Order lifecycle management
├── cart/         # Shopping cart (Redis-backed)
├── users/        # Custom user model, auth
├── payments/     # MercadoPago integration
├── shipping/     # Shipping calculation
└── admin/        # Custom admin dashboard
```

## Database Models

Each app follows the pattern:
- `models.py` — ORM models
- `admin.py` — Admin registrations
- `api/` — DRF viewsets and serializers
- `tests/` — pytest tests

## Running Celery (Dev)

```bash
celery -A core worker -l info
celery -A core beat -l info  # scheduled tasks
```

## Cache Strategy

- Product listings: 15 min TTL
- Session data: Redis sessions
- Rate limiting: Redis counters
