# Architecture Overview

## Tech Stack

- **Backend:** Django 4.x
- **Database:** PostgreSQL
- **Cache:** Redis
- **Web Server:** Nginx
- **Container:** Docker + Docker Compose

## Project Structure

```
apps/
├── products/       # Product catalog
├── orders/         # Order management
├── users/          # User authentication
└── payments/       # Payment processing
core/
├── settings.py     # Django settings
└── urls.py         # URL routing
```

## Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for deployment instructions.
