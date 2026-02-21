<div align="center">

# 🏢 ECOMMDEV Platform

[![Django](https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.15-red?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![Security](https://img.shields.io/badge/Security-OWASP_Compliant-27ae60?style=for-the-badge&logo=owasp&logoColor=white)](https://owasp.org)
[![Live](https://img.shields.io/badge/🌐_Live_Production-ecommdev.com.br-0a66c2?style=for-the-badge)](https://www.ecommdev.com.br)

**Enterprise-grade web development agency platform with client management, billing, and project tracking.**

🔗 **Production site:** [www.ecommdev.com.br](https://www.ecommdev.com.br)

[Architecture](#-architecture) · [Features](#-features) · [Tech Stack](#-tech-stack) · [Quick Start](#-quick-start) · [API Docs](#-api-documentation) · [Security](#-security)

</div>

---

## 📋 Overview

ECOMMDEV is a full-stack Django platform built for a professional web development agency. It handles the complete business lifecycle — from client onboarding to project delivery, invoicing, and support ticketing. Built with security-first principles and designed to scale.

> ⚠️ **Note:** This is a **demo/showcase version** of the production platform. Sensitive business logic, client data, and API keys have been removed. The full production system is deployed and serving real clients.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      NGINX (Reverse Proxy)               │
│                   SSL/TLS Termination                    │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                  Django Application                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────┐  │
│  │  Clients │ │ Projects │ │ Invoices │ │  Support  │  │
│  └──────────┘ └──────────┘ └──────────┘ └───────────┘  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────┐  │
│  │ Services │ │ Packages │ │Portfolio │ │Quotations │  │
│  └──────────┘ └──────────┘ └──────────┘ └───────────┘  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────┐  │
│  │   API    │ │  Notif.  │ │   Core   │ │   i18n    │  │
│  └──────────┘ └──────────┘ └──────────┘ └───────────┘  │
│                  Django REST Framework                    │
└────────┬───────────────┬────────────────┬───────────────┘
         │               │                │
┌────────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
│ PostgreSQL 16 │ │  Redis 7    │ │   Celery    │
│   Database    │ │ Cache/Queue │ │   Workers   │
└───────────────┘ └─────────────┘ └─────────────┘
```

---

## ✨ Features

### 🧩 13 Django Modules

| Module | Description |
|--------|-------------|
| **👥 Clients** | Client onboarding, profiles, and relationship management |
| **📁 Projects** | Project lifecycle management with milestones and deadlines |
| **💰 Invoices** | Automated billing with MercadoPago payment integration |
| **📋 Quotations** | Professional quote generation and approval workflow |
| **📦 Packages** | Service packages with tiered pricing |
| **🛠️ Services** | Service catalog management |
| **🎨 Portfolio** | Public portfolio showcase for completed projects |
| **🎫 Support** | Ticket system for client support |
| **🔔 Notifications** | Real-time notification system (email + in-app) |
| **🌐 API** | RESTful API (DRF) with JWT authentication |
| **⚙️ Core** | Base models, middlewares, utilities, health checks |
| **🌍 i18n** | Internationalization (pt-BR, en-US) |
| **📊 Analytics** | Google Analytics integration |

### 🔒 Security Features
- **OWASP Compliant** — SQL injection, XSS, CSRF protected
- **JWT Authentication** — Stateless API auth with token refresh
- **Rate Limiting** — Custom limiter (login: 5/min, register: 3/min, API: 100/h anon, 1000/h auth)
- **Password Security** — 4 validators, min 8 chars, complexity rules
- **HSTS + Secure Cookies** — Full SSL enforcement in production
- **Webhook HMAC** — Signature verification on payment webhooks
- **Security Audit Score: GOOD** — Professional security audit completed

### 💳 Payment Integration
- **MercadoPago** — Brazilian payment gateway
- Invoice generation with automatic payment tracking
- Webhook-based payment status updates
- Refund processing

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Django 4.2 + Django REST Framework |
| **Database** | PostgreSQL 16 |
| **Cache** | Redis 7 |
| **Task Queue** | Celery + Redis Broker |
| **Web Server** | Nginx (reverse proxy + static files) |
| **Containerization** | Docker + Docker Compose (6 services) |
| **Authentication** | JWT (SimpleJWT) + Session Auth |
| **Payments** | MercadoPago SDK |
| **Storage** | AWS S3 (production) / Local (dev) |
| **Monitoring** | Health checks + structured logging |
| **i18n** | Django i18n (pt-BR, en-US) |

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/kelsonbrito50/ecommdev-demo.git
cd ecommdev-demo

# Copy environment variables
cp .env.example .env

# Start all services (Django + PostgreSQL + Redis + Nginx + Celery)
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access the application
# Web:  http://localhost:8000
# API:  http://localhost:8000/api/v1/
# Admin: http://localhost:8000/admin/
```

---

## 📡 API Documentation

### Authentication
```http
POST /api/v1/auth/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}

# Response
{
  "access": "eyJhbGciOiJIUzI1NiIs...",
  "refresh": "eyJhbGciOiJIUzI1NiIs...",
  "user": { "id": 1, "email": "user@example.com" }
}
```

### Endpoints Overview
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/auth/login/` | JWT login |
| `POST` | `/api/v1/auth/refresh/` | Refresh token |
| `GET` | `/api/v1/clients/` | List clients |
| `POST` | `/api/v1/projects/` | Create project |
| `GET` | `/api/v1/invoices/` | List invoices |
| `POST` | `/api/v1/quotations/` | Generate quote |
| `GET` | `/api/v1/services/` | List services |
| `GET` | `/api/v1/portfolio/` | Public portfolio |
| `POST` | `/api/v1/support/tickets/` | Create support ticket |
| `GET` | `/api/v1/health/` | Health check |

### Rate Limits
| Scope | Limit |
|-------|-------|
| Anonymous | 100 requests/hour |
| Authenticated | 1,000 requests/hour |
| Login | 5 attempts/minute |
| Register | 3 attempts/minute |

---

## 🔒 Security

This platform was built following OWASP security guidelines:

| Check | Status |
|-------|--------|
| SQL Injection | ✅ Protected (Django ORM, no raw SQL) |
| XSS | ✅ Protected (auto-escaping, no unsafe marks) |
| CSRF | ✅ Protected (middleware + token validation) |
| Authentication | ✅ JWT + Session with hash rotation |
| Rate Limiting | ✅ Custom middleware per endpoint |
| HTTPS | ✅ HSTS + secure cookies in production |
| Password | ✅ 4 validators + complexity rules |
| API Throttling | ✅ Per-user and per-IP limits |

> Full security audit report available upon request.

---

## 📊 Project Metrics

- **13 Django modules** — Complete business platform
- **6 Docker containers** — Fully containerized architecture
- **2 languages** — Internationalized (pt-BR, en-US)
- **Security score: GOOD** — Professional audit completed
- **API endpoints: 20+** — RESTful with full CRUD
- **Test coverage: Growing** — Unit + integration tests

---

## 📐 Docker Architecture

```yaml
Services:
  web:        Django application (Gunicorn)
  db:         PostgreSQL 16 Alpine
  redis:      Redis 7 Alpine (cache + message broker)
  celery:     Celery worker (async tasks)
  nginx:      Reverse proxy + static file serving
  beat:       Celery Beat (scheduled tasks)
```

---

## 🤝 About

Built by **Kelson Brito** as the core platform for [ECOMMDEV](https://www.ecommdev.com.br/), a professional web development agency.

This demo showcases the architecture, security practices, and engineering decisions behind a real production system serving actual clients.

---

## 📄 License

This demo version is MIT licensed. The production platform is proprietary.

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
