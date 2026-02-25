<div align="center">

# ⚡ ECOMMDEV Platform

### Enterprise Django Platform — Built for Scale, Engineered for Production

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.14-red?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![AWS S3](https://img.shields.io/badge/AWS-S3-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)](https://aws.amazon.com/s3/)
[![OWASP](https://img.shields.io/badge/OWASP-Compliant-000000?style=for-the-badge&logo=owasp&logoColor=white)](https://owasp.org)
[![Security Audit](https://img.shields.io/badge/Security%20Audit-GOOD-brightgreen?style=for-the-badge&logo=shieldsdotio&logoColor=white)](https://www.ecommdev.com.br/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](./LICENSE)

<br/>

**[🌐 Website](https://www.ecommdev.com.br/)** · **[📦 Modules](#-modules)** · **[🚀 Quick Start](#-quick-start)** · **[🔒 Security](#-security)**

<br/>

> 🌐 **Production system live at [ecommdev.com.br](https://www.ecommdev.com.br/).** Sensitive configs excluded for security.

</div>

---

## 🧭 About

**ECOMMDEV Platform** is the core operational backbone of [ECOMMDEV](https://www.ecommdev.com.br/) — a web development agency. It is an **enterprise-grade Django monolith** architected to handle real-world business complexity: multi-tenant client management, async task processing, payment orchestration, and a rich internal admin surface.

This repository contains the public codebase — cleaned and documented to reflect the engineering standards powering the agency's operations.

### 📊 Platform at a Glance

| Metric | Value |
|---|---|
| 🧩 Business Modules | **13** |
| 🐳 Docker Containers | **6** |
| 🔌 REST API Endpoints | **50+** |
| ⚙️ Async Task Queues | **Celery + Redis** |
| 📂 File Storage | **AWS S3** |
| 💳 Payment Provider | **MercadoPago** |
| 🔒 Security Rating | **GOOD (OWASP Audit)** |
| 🧪 Architecture | **Monolith + Async Workers** |

---

## 🧩 Modules

The platform is organized into **13 independent business modules**, each with isolated logic, models, serializers, and API routes.

| # | Module | Description |
|---|---|---|
| 1 | 🔐 **Authentication** | JWT-based auth, OAuth2 support, session management, role & permission system |
| 2 | 📦 **Products** | Full product catalog with categories, variants, pricing rules, and S3 image management |
| 3 | 🛒 **Orders** | Order lifecycle management — creation, tracking, cancellation, history |
| 4 | 💳 **Payments** | MercadoPago integration, webhook handling, payment status tracking, refund flows |
| 5 | 👥 **CRM** | Client relationship management — contacts, pipelines, deal tracking, notes |
| 6 | 📈 **Analytics** | Business intelligence layer — sales KPIs, traffic insights, conversion metrics |
| 7 | 🔔 **Notifications** | Multi-channel notification system (in-app, email) via Celery async tasks |
| 8 | 🛠️ **Admin** | Custom Django admin with dashboards, bulk actions, and audit logging |
| 9 | 🌐 **API** | Centralized DRF API gateway — versioning, throttling, schema (OpenAPI/Swagger) |
| 10 | 🔍 **Search** | Full-text search across products, orders, and clients with filtering and ranking |
| 11 | 📊 **Reports** | Scheduled and on-demand report generation with export (PDF/CSV) |
| 12 | 🔗 **Integrations** | Third-party service connectors — webhooks, event bus, external API adapters |
| 13 | 🛡️ **Security** | Audit logging, rate limiting, IP filtering, token rotation, intrusion detection hooks |

---

## 🛠️ Tech Stack

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| **Backend** | Django | 4.2 LTS | Core web framework |
| **API** | Django REST Framework | 3.14 | RESTful API layer |
| **Frontend** | React | 18 | Admin UI & client-facing views |
| **Database** | PostgreSQL | 16 | Primary relational database |
| **Cache / Broker** | Redis | 7 | Session cache, Celery message broker |
| **Task Queue** | Celery | 5.x | Async job processing (worker + beat) |
| **File Storage** | AWS S3 | — | Static & media file storage |
| **Payments** | MercadoPago API | v2 | Payment processing & webhooks |
| **Reverse Proxy** | Nginx | 1.25 | TLS termination, static serving |
| **Containerization** | Docker + Compose | — | Full-stack local & production environment |
| **Auth** | JWT + OAuth2 | — | Stateless authentication |
| **API Docs** | drf-spectacular | — | OpenAPI 3.0 schema auto-generation |

---

## 🏗️ Architecture

The platform runs as a **6-container Docker Compose stack**, with clean service separation:

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Compose Stack                  │
│                                                         │
│  ┌─────────┐     ┌─────────────────────────────────┐   │
│  │  nginx  │────▶│           web (Django)           │   │
│  │  :80    │     │        Gunicorn / ASGI           │   │
│  │  :443   │     └────────────┬────────────────┬────┘   │
│  └─────────┘                  │                │        │
│                               │                │        │
│             ┌─────────────────▼──┐    ┌────────▼──────┐ │
│             │   db (PostgreSQL)  │    │  redis (Cache/ │ │
│             │       :5432        │    │   Broker) :6379│ │
│             └────────────────────┘    └───────┬────────┘ │
│                                               │          │
│                          ┌────────────────────┴───────┐  │
│                          │                            │  │
│               ┌──────────▼─────┐    ┌────────────────▼┐ │
│               │ celery-worker  │    │   celery-beat   │ │
│               │ (async tasks)  │    │ (scheduled jobs)│ │
│               └────────────────┘    └─────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Container Responsibilities

| Container | Role |
|---|---|
| `nginx` | Reverse proxy, SSL termination, static file serving |
| `web` | Django application server (Gunicorn) |
| `db` | PostgreSQL 16 — persistent relational storage |
| `redis` | Cache backend + Celery message broker |
| `celery-worker` | Processes async tasks (emails, reports, webhooks) |
| `celery-beat` | Scheduler for periodic/cron-style tasks |

---

## 🔒 Security

Security is a **first-class concern** in this platform, not an afterthought.

### OWASP Compliance

The platform is built to address the **OWASP Top 10** attack vectors:

| OWASP Risk | Mitigation |
|---|---|
| A01 — Broken Access Control | Role-based permissions, object-level access via DRF |
| A02 — Cryptographic Failures | Secrets via env vars, HTTPS enforced, no plaintext credentials |
| A03 — Injection | ORM-only queries, parameterized inputs, no raw SQL |
| A04 — Insecure Design | Principle of least privilege across all modules |
| A05 — Security Misconfiguration | Hardened `settings.py`, Docker secrets, no debug in prod |
| A06 — Vulnerable Components | Dependency pinning + regular `pip audit` checks |
| A07 — Auth Failures | JWT + refresh rotation, brute-force rate limiting |
| A08 — Software Integrity | Docker image pinning, no untrusted third-party scripts |
| A09 — Logging Failures | Centralized audit logging module, failed auth alerts |
| A10 — SSRF | Validated outgoing request domains, no open redirects |

### Audit Result

```
┌─────────────────────────────────────────┐
│         SECURITY AUDIT SUMMARY          │
│                                         │
│   Overall Rating:   ██████████  GOOD    │
│   OWASP Compliant:  ✅ YES              │
│   Auth Security:    ✅ STRONG           │
│   Data Exposure:    ✅ NONE DETECTED    │
│   Injection Risk:   ✅ MITIGATED        │
│   Config Hardening: ✅ APPLIED          │
└─────────────────────────────────────────┘
```

### Additional Hardening

- `SECURE_HSTS_SECONDS`, `X_FRAME_OPTIONS`, `SECURE_CONTENT_TYPE_NOSNIFF` enforced
- CORS policy restricted to trusted origins
- API rate limiting via DRF throttling
- Admin panel restricted by IP allowlist in production
- Celery tasks signed and validated
- AWS S3 bucket policies enforce private access by default

---

## 🚀 Quick Start

### Prerequisites

- Docker + Docker Compose v2
- Git
- (Optional) Make

### 1. Clone the Repository

```bash
git clone https://github.com/kelsonbrito50/ecommdev-platform.git
cd ecommdev-platform
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and fill in your values:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
POSTGRES_DB=ecommdev
POSTGRES_USER=ecommdev
POSTGRES_PASSWORD=strongpassword

# Redis
REDIS_URL=redis://redis:6379/0

# AWS S3
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_STORAGE_BUCKET_NAME=your-bucket

# MercadoPago
MERCADOPAGO_ACCESS_TOKEN=your-token
```

### 3. Build & Launch

```bash
docker compose up --build
```

### 4. Initialize the Database

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py collectstatic --noinput
```

### 5. Access the Platform

| Service | URL |
|---|---|
| Django App | http://localhost:8000 |
| Admin Panel | http://localhost:8000/admin |
| API Schema (Swagger) | http://localhost:8000/api/schema/swagger-ui/ |
| API Schema (ReDoc) | http://localhost:8000/api/schema/redoc/ |

---

## 📁 Project Structure

```
ecommdev-platform/
├── config/                  # Django settings (base, dev, prod)
├── apps/
│   ├── authentication/      # Module 01 — Auth & permissions
│   ├── products/            # Module 02 — Product catalog
│   ├── orders/              # Module 03 — Order management
│   ├── payments/            # Module 04 — MercadoPago integration
│   ├── crm/                 # Module 05 — CRM & client pipeline
│   ├── analytics/           # Module 06 — KPIs & insights
│   ├── notifications/       # Module 07 — Notification engine
│   ├── admin_panel/         # Module 08 — Custom admin
│   ├── api/                 # Module 09 — API gateway
│   ├── search/              # Module 10 — Full-text search
│   ├── reports/             # Module 11 — Report generation
│   ├── integrations/        # Module 12 — External connectors
│   └── security/            # Module 13 — Security & audit
├── frontend/                # React app
├── docker/                  # Dockerfiles per service
├── docker-compose.yml       # Full stack definition
├── docker-compose.prod.yml  # Production overrides
├── nginx/                   # Nginx config
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── manage.py
└── .env.example
```

---

## 🧠 What I Learned

Building this platform end-to-end was a deep exercise in **real-world software engineering**. Key takeaways:

**Backend Architecture**
- Designing a modular Django monolith that stays maintainable as it grows — the balance between monolith simplicity and bounded context isolation
- Django REST Framework's power for building robust, self-documenting APIs
- Celery's architecture for reliable async task processing, including beat scheduling, task retries, and dead-letter handling

**Infrastructure & DevOps**
- Composing multi-service Docker environments that mirror production exactly
- Nginx configuration for SSL termination, WebSocket proxying, and static file caching
- AWS S3 integration for scalable file storage with proper IAM policies

**Security Engineering**
- Implementing OWASP Top 10 mitigations systematically, not as an afterthought
- JWT token rotation patterns that balance security with user experience
- Building an audit logging system that captures who did what, when, and from where

**Payment Integration**
- MercadoPago's webhook architecture and idempotency requirements
- Handling payment edge cases: partial refunds, expired sessions, concurrent requests
- Building a provider-agnostic payment layer that could swap to Stripe or PayPal with minimal changes

**Team & Process**
- Structuring a Django project for team collaboration — clear module boundaries, consistent patterns
- Writing documentation that developers actually read (hint: keep it close to the code)

---

## License

This project is licensed under the [MIT License](./LICENSE).

---

<div align="center">

Built by **[Kelson Brito](https://github.com/kelsonbrito50)** — Founder @ [ECOMMDEV](https://www.ecommdev.com.br/)

⭐ Star this repo if you find it useful.

</div>
