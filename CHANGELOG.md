# Changelog

All notable changes to ECOMMDEV are documented here.  
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- GitHub Actions CI/CD pipeline (`ci.yml`) with lint, test, security, and docker jobs
- Multi-stage Dockerfile with non-root user and HEALTHCHECK (already present, documented)
- Optimized `.dockerignore` — excludes dev artifacts, scripts, fixtures from image
- Comprehensive `README.md` — bilingual (EN/PT-BR), architecture diagram, API reference
- `CHANGELOG.md` — this file
- Security tools: `ruff`, `bandit`, `safety` added to `requirements.txt`

---

## [1.3.0] — 2026-01-28

### Added
- Management commands for auto-updating service prices, portfolio, and testimonials
- Webhook security fix: HMAC signature now **required** (no longer optional)

### Security
- `core/webhook.py`: GitHub webhook now blocks execution if `GITHUB_WEBHOOK_SECRET` is not set

---

## [1.2.0] — 2026-01-25

### Fixed
- i18n: Removed `#, fuzzy` flag from `pt_BR.po`; completed English translations
- FAQ page: Added missing model properties and category filter
- Hardcoded Portuguese text replaced with `gettext` calls across templates

### Changed
- Social links updated; removed WhatsApp contact option
- Language-aware model properties added for bilingual display

---

## [1.1.0] — 2026-01-22

### Fixed (38 bugs)
- Full project audit: fixed bugs across models, views, templates, and migration scripts
- CSRF: Skip session rotation in admin to fix logout issue
- Missing migrations added; validator serialization fixed
- Portfolio admin: Fixed 500 errors (JSONField search, null handling)
- Pacotes admin: Simplified to fix 500 error
- Registration: Fixed 500 error when email delivery fails; added error logging
- Support ticket detail: Handle `null` author gracefully
- `CaseImage.__str__`: Fixed null handling

### Changed
- Simplified portfolio and pacotes admin pages for reliability
- Added language-aware model properties (`titulo`, `descricao`, etc.)

### Security
- Added CDN (`cdn.jsdelivr.net`) to Content Security Policy `connect-src`

---

## [1.0.0] — 2026-01-10

### Added
- **core**: Homepage, About, Contact, FAQ, Privacy Policy, Terms, XML Sitemap
- **servicos**: Service catalog with pricing tiers
- **pacotes**: Package / subscription plans
- **orcamentos**: Quote request form with email notification
- **portfolio**: Cases with multi-image support and technology tags
- **clientes**: Client registration, JWT + session auth, email verification, profile management, active session management
- **projetos**: Project dashboard with file uploads, timeline milestones, and messaging
- **suporte**: Support ticket system with staff responses
- **faturas**: Invoice management with MercadoPago payment integration
- **notificacoes**: In-app notification system
- **api**: REST API v1 with DRF ViewSets + JWT auth + rate throttling
- **admin**: Custom-branded Django admin with obscured URL (`/gerenciar-ecd/`)
- Docker Compose setup (dev + production)
- Nginx configuration with SSL and static file serving
- Celery worker configuration with Redis broker
- Full bilingual support (PT-BR / EN) via Django i18n
- Rate limiting middleware: 5/min login, 3/min register
- HSTS, secure cookies, CSP, XFrame-Options for production security

---

## Legend

- **Added** — New features
- **Changed** — Changes to existing functionality
- **Deprecated** — Features that will be removed in a future release
- **Removed** — Removed features
- **Fixed** — Bug fixes
- **Security** — Security patches or improvements

[Unreleased]: https://github.com/ecommdev/ecommdev/compare/v1.3.0...HEAD
[1.3.0]: https://github.com/ecommdev/ecommdev/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/ecommdev/ecommdev/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/ecommdev/ecommdev/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/ecommdev/ecommdev/releases/tag/v1.0.0
