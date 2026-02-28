# ECOMMDEV — Web Development Agency Platform

> **EN** | [**PT-BR** ↓](#pt-br)

[![CI](https://github.com/ecommdev/ecommdev/actions/workflows/ci.yml/badge.svg)](https://github.com/ecommdev/ecommdev/actions/workflows/ci.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/django-6.0-green.svg)](https://djangoproject.com)
[![License: Proprietary](https://img.shields.io/badge/license-Proprietary-red.svg)](#license)

---

## Overview

**ECOMMDEV** is a full-featured agency management platform built with Django 6.0. It powers the complete lifecycle of a web development agency — from service catalog and quote requests to client dashboards, project tracking, support tickets, and invoicing.

Supports **English** and **Brazilian Portuguese** (i18n/l10n via Django's i18n framework).

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 6.0.1, Django REST Framework 3.14 |
| Auth | JWT (SimpleJWT) + Session Auth |
| Database | PostgreSQL 16 |
| Cache / Broker | Redis 7 |
| Background Tasks | Celery 5.3 |
| Web Server | Nginx + Gunicorn 21 |
| Containerization | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Payments | MercadoPago |
| Email | Django Anymail |
| Storage | AWS S3 (django-storages + boto3) |
| Code Quality | Ruff, Black, isort |
| Security | Bandit, Safety |

---

## Modules (12)

| # | Module | Description |
|---|--------|-------------|
| 1 | **core** | Homepage, About, FAQ, Contact, Privacy, Terms, Sitemaps |
| 2 | **servicos** | Service catalog with pricing and descriptions |
| 3 | **pacotes** | Service packages / subscription plans |
| 4 | **orcamentos** | Quote request form and management |
| 5 | **portfolio** | Portfolio cases with images and technology tags |
| 6 | **clientes** | Client registration, auth, profile, email verification |
| 7 | **projetos** | Project dashboard, files, timeline, messages |
| 8 | **suporte** | Support ticket system |
| 9 | **faturas** | Invoices, billing history, MercadoPago payments |
| 10 | **notificacoes** | In-app notification system |
| 11 | **api** | REST API v1 (DRF + JWT) |
| 12 | **admin** | Custom Django admin (obscured URL, branding) |

---

## Features

- 🌐 **Bilingual** — full PT-BR / EN support via Django i18n
- 🔐 **JWT + Session Auth** — dual auth strategy (API + web)
- 📋 **Quote Workflow** — client submits → admin manages → project created
- 📂 **Project Dashboard** — file uploads, timeline, real-time messages
- 💳 **Integrated Billing** — MercadoPago payments, invoice history
- 🎫 **Support Tickets** — clients open/track tickets with staff responses
- 📬 **Email Notifications** — transactional emails via Anymail
- 🔔 **In-App Notifications** — real-time notification system
- 🖼️ **Portfolio CMS** — showcases with images, tech stack, categories
- 📦 **Package Plans** — tiered service packages with feature lists
- 🛡️ **Security Hardened** — HSTS, CSP, rate limiting, CSRF protection
- 📊 **Django Admin** — custom-branded admin panel (obscured URL)
- 🌍 **Sitemap** — auto-generated XML sitemap for SEO
- 🐳 **Docker Ready** — multi-stage build, non-root user, healthcheck

---

## Quick Start with Docker

### Prerequisites
- Docker 24+ and Docker Compose v2
- Git

### 1. Clone & Configure

```bash
git clone https://github.com/ecommdev/ecommdev.git
cd ecommdev

# Copy and configure environment
cp .env.example .env
# Edit .env with your settings (SECRET_KEY, DB credentials, etc.)
```

### 2. Start (Development)

```bash
docker compose -f docker-compose.dev.yml up --build
```

The app will be available at **http://localhost:8000**

### 3. Start (Production)

```bash
docker compose up -d --build
```

### 4. Initial Setup

```bash
# Run migrations
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser

# Load sample data (optional)
docker compose exec web python manage.py loaddata fixtures/initial_data.json

# Collect static files
docker compose exec web python manage.py collectstatic --noinput
```

### 5. Admin Panel

Navigate to `/gerenciar-ecd/` with your superuser credentials.

---

## Local Development (without Docker)

```bash
# Create virtualenv
python -m venv venv && source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment
export DEBUG=True
export SECRET_KEY=your-dev-key
export DATABASE_URL=postgresql://user:pass@localhost/ecommdev

# Migrate & run
python manage.py migrate
python manage.py runserver
```

---

## Architecture Overview

```
                         ┌─────────────┐
                         │  Certbot    │  (SSL cert renewal)
                         └──────┬──────┘
                                │ certs
                         ┌──────▼──────┐
          HTTP/HTTPS     │    Nginx    │  static/media served directly
  Browser ──────────────▶│  (reverse   │
                         │   proxy)    │
                         └──────┬──────┘
                                │
                         ┌──────▼──────┐
                         │  Gunicorn   │  (4 sync workers)
                         └──────┬──────┘
                                │
                         ┌──────▼──────┐
                         │   Django    │  business logic / templates / ORM
                         │   6.0.1     │
                         └──┬──┬───┬───┘
                            │  │   │
              ┌─────────────┘  │   └──────────────────┐
              │                │                      │
       ┌──────▼──┐      ┌──────▼──┐           ┌──────▼──────┐
       │Postgres │      │  Redis  │           │   Celery    │
       │   16    │      │    7    │◀──broker──│Worker+Beat  │
       │(primary │      │ (cache) │           │(async tasks)│
       │  store) │      └─────────┘           └─────────────┘
       └─────────┘
```

**Request Flow:**

1. `Certbot` — auto-renews Let's Encrypt TLS certificates every 12 hours
2. `Nginx` — terminates SSL/TLS, serves `staticfiles/` and `media/` directly (zero Django overhead)
3. `Gunicorn` — forwards dynamic requests to Django (4 sync workers)
4. `Django 6.0.1` — processes business logic, ORM queries, and renders templates
5. `PostgreSQL 16` — primary relational data store (all models)
6. `Redis 7` — dual role: cache backend (sessions, query results) + Celery message broker
7. `Celery Worker` — processes async tasks (transactional emails, notifications, reports)
8. `Celery Beat` — scheduler for periodic tasks (cleanup, reminders, analytics aggregation)

---

## API Versioning Strategy

ECOMMDEV uses **URL-based versioning** for its REST API:

| Version | Base URL | Status |
|---------|----------|--------|
| v1 | `/api/v1/` | ✅ Current (stable) |
| v2 | `/api/v2/` | 🚧 Planned |

### Versioning Rules

1. **URL prefix** — version is embedded in the path: `/api/v1/resource/`
2. **No breaking changes within a version** — backward-compatible additions (new fields, new endpoints) are allowed without bumping the version
3. **Breaking changes require a new version** — removing fields, changing data types, or altering authentication requirements always introduce a new version (e.g., `/api/v2/`)
4. **Deprecation period** — old versions are supported for a minimum of **6 months** after a new version is released
5. **Sunset headers** — deprecated endpoints return `Sunset: <date>` and `Link: </api/v2/resource/>; rel="successor-version"` headers

### Adding a New API Version

```python
# api/urls.py — register both versions
path('api/v1/', include('api.v1.urls')),
path('api/v2/', include('api.v2.urls')),
```

Versioned modules live under `api/v1/`, `api/v2/`, etc., each with its own serializers, views, and URLs.

### Versioning FAQ

**Q: Why URL versioning instead of headers?**  
URL versioning is easier to test in a browser, simpler to cache, and more explicit for clients. Header versioning (e.g., `Accept: application/vnd.ecommdev.v2+json`) is reserved for future consideration.

**Q: Will v1 be removed?**  
Not without a 6-month deprecation notice. Watch the CHANGELOG for announcements.

---

## API Endpoints

Base URL: `/api/v1/`

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/login/` | Obtain JWT token pair |
| POST | `/api/v1/auth/refresh/` | Refresh JWT access token |

### REST Resources (DRF ViewSets)

| Resource | Endpoint | Auth Required |
|----------|----------|---------------|
| Services | `/api/v1/servicos/` | No |
| Packages | `/api/v1/pacotes/` | No |
| Portfolio | `/api/v1/portfolio/` | No |
| Quotes | `/api/v1/orcamentos/` | Yes |
| Projects | `/api/v1/projetos/` | Yes |
| Tickets | `/api/v1/tickets/` | Yes |
| Invoices | `/api/v1/faturas/` | Yes |
| Client Profile | `/api/v1/clientes/me/` | Yes |
| Contact | `/api/v1/contato/` | No |
| Notifications | `/api/v1/notificacoes/` | Yes |

**Authentication:** Bearer JWT token in `Authorization: Bearer <token>` header.

**Throttling:**
- Anonymous: 100 requests/hour
- Authenticated: 1000 requests/hour

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | ✅ Prod | dev-key | Django secret key |
| `DEBUG` | No | `False` | Enable debug mode |
| `ALLOWED_HOSTS` | ✅ Prod | `localhost` | Comma-separated hostnames |
| `DB_NAME` | ✅ | `ecommdev` | PostgreSQL database name |
| `DB_USER` | ✅ | `postgres` | PostgreSQL user |
| `DB_PASSWORD` | ✅ | — | PostgreSQL password |
| `DB_HOST` | ✅ | `localhost` | PostgreSQL host |
| `DB_PORT` | No | `5432` | PostgreSQL port |
| `REDIS_URL` | ✅ | `redis://localhost:6379/0` | Redis connection URL |
| `EMAIL_HOST` | Prod | — | SMTP host |
| `MERCADOPAGO_ACCESS_TOKEN` | Prod | — | MercadoPago API token |
| `AWS_ACCESS_KEY_ID` | Prod | — | S3 storage key |
| `AWS_SECRET_ACCESS_KEY` | Prod | — | S3 storage secret |
| `GITHUB_WEBHOOK_SECRET` | ✅ Prod | — | GitHub deploy webhook HMAC secret |

---

## Security

**Security Audit Rating: GOOD** _(conducted 2026-01-22)_

| Category | Status |
|----------|--------|
| SQL Injection | ✅ Protected (Django ORM only) |
| XSS | ✅ Protected (auto-escaping, no `\|safe`) |
| CSRF | ✅ Protected (middleware + tokens) |
| Password Security | ✅ Strong (4 validators, min 8 chars) |
| Rate Limiting | ✅ Implemented (5/min login, 3/min register) |
| HSTS / Secure Cookies | ✅ Enabled in production |
| JWT Auth | ✅ Configured with throttling |
| Session Security | ✅ Hash updated on password change |
| Webhook Security | ✅ Fixed — HMAC verification enforced |

See [`SECURITY_AUDIT_REPORT.md`](SECURITY_AUDIT_REPORT.md) for full details.

---

## Testing

```bash
# Run all tests
python manage.py test --verbosity=2

# With coverage
coverage run manage.py test && coverage report

# Run specific app
python manage.py test clientes.tests
```

---

## CI/CD Pipeline

GitHub Actions runs on every push/PR to `main` or `develop`:

1. **Lint** — `ruff check` + format validation
2. **Test** — Django tests against PostgreSQL 16 + Redis (with coverage ≥ 85%)
3. **Security** — Bandit (SAST) + Safety (dependency CVE scan)
4. **Docker** — Validate `docker-compose.yml` syntax _(main branch only)_

---

## License

**Proprietary** — All rights reserved.

Copyright © 2026 Kelson Brito / ECOMMDEV. No part of this software may be reproduced, distributed, or modified without prior written permission.

---

---

<a name="pt-br"></a>

# ECOMMDEV — Plataforma de Agência de Desenvolvimento Web

> [**EN** ↑](#ecommdev--web-development-agency-platform) | **PT-BR**

---

## Visão Geral

**ECOMMDEV** é uma plataforma completa de gestão para agência de desenvolvimento web, construída com Django 6.0. Gerencia o ciclo completo da agência — do catálogo de serviços e solicitações de orçamento até dashboards de clientes, acompanhamento de projetos, tickets de suporte e faturamento.

Suporta **inglês** e **português brasileiro** (i18n/l10n via framework i18n do Django).

---

## Stack Tecnológica

| Camada | Tecnologia |
|--------|-----------|
| Backend | Django 6.0.1, Django REST Framework 3.14 |
| Autenticação | JWT (SimpleJWT) + Sessão |
| Banco de Dados | PostgreSQL 16 |
| Cache / Broker | Redis 7 |
| Tarefas em Background | Celery 5.3 |
| Servidor Web | Nginx + Gunicorn 21 |
| Containerização | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Pagamentos | MercadoPago |
| E-mail | Django Anymail |
| Armazenamento | AWS S3 (django-storages + boto3) |

---

## Módulos (12)

| # | Módulo | Descrição |
|---|--------|-----------|
| 1 | **core** | Página inicial, Sobre, FAQ, Contato, Privacidade, Termos, Sitemaps |
| 2 | **servicos** | Catálogo de serviços com preços e descrições |
| 3 | **pacotes** | Pacotes de serviços / planos de assinatura |
| 4 | **orcamentos** | Formulário e gestão de pedidos de orçamento |
| 5 | **portfolio** | Cases de portfólio com imagens e tags de tecnologia |
| 6 | **clientes** | Cadastro, autenticação, perfil e verificação de e-mail |
| 7 | **projetos** | Dashboard de projetos, arquivos, timeline, mensagens |
| 8 | **suporte** | Sistema de tickets de suporte |
| 9 | **faturas** | Faturas, histórico de pagamentos, integração MercadoPago |
| 10 | **notificacoes** | Sistema de notificações in-app |
| 11 | **api** | REST API v1 (DRF + JWT) |
| 12 | **admin** | Django Admin customizado (URL obscurecida, branding) |

---

## Início Rápido com Docker

```bash
# Clone o projeto
git clone https://github.com/ecommdev/ecommdev.git
cd ecommdev

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas configurações

# Suba o ambiente de desenvolvimento
docker compose -f docker-compose.dev.yml up --build

# Execute as migrações
docker compose exec web python manage.py migrate

# Crie o superusuário
docker compose exec web python manage.py createsuperuser
```

Acesse em **http://localhost:8000** | Admin em **http://localhost:8000/gerenciar-ecd/**

---

## Segurança

**Avaliação da Auditoria de Segurança: BOA** _(realizada em 22/01/2026)_

Veja [`SECURITY_AUDIT_REPORT.md`](SECURITY_AUDIT_REPORT.md) para o relatório completo.

---

## Licença

**Proprietária** — Todos os direitos reservados.

Copyright © 2026 Kelson Brito / ECOMMDEV. Nenhuma parte deste software pode ser reproduzida, distribuída ou modificada sem permissão prévia por escrito.
