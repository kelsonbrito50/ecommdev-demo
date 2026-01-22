# ECOMMDEV - Web Development Agency Platform

## 🌐 **www.ecommdev.com.br**

Sistema completo de agência de desenvolvimento web para pequenas e médias empresas em João Pessoa/PB.

### 📋 Visão Geral

Plataforma bilíngue (PT-BR/EN) com **Modern UI/UX Design System** e:
- Site institucional responsivo
- Sistema de pacotes e orçamentos
- Área do cliente (Dashboard)
- Painel administrativo
- Blog e Portfólio
- REST API completa
- Sistema de tickets de suporte
- Faturamento e pagamentos
- **Acessibilidade WCAG 2.1 AA**
- **Mobile-First Design**
- **Dark Mode Support**

---

## 🎨 UI/UX Design System

### Design Principles

**1. Modern & Clean**
- Glassmorphism effects
- Smooth animations and transitions
- Gradient accents
- Micro-interactions
- Neumorphism subtle shadows

**2. Mobile-First Responsive**
- Breakpoints: 320px, 768px, 1024px, 1440px
- Touch-optimized (44px+ touch targets)
- Swipe gestures support
- Adaptive layouts

**3. Accessibility-First (WCAG 2.1 AA)**
- Semantic HTML5
- ARIA labels and roles
- Keyboard navigation support
- Screen reader compatible
- High contrast mode
- Focus indicators
- Skip navigation links

**4. Performance Optimized**
- Lazy loading images
- Code splitting
- CSS/JS minification
- Browser caching
- CDN for static assets
- WebP images with fallbacks

### Color System

```css
/* Primary Colors */
--brand-blue: #0066CC;
--brand-dark: #1a1a2e;
--accent-orange: #FF6B35;

/* Secondary Colors */
--success-green: #28a745;
--warning-yellow: #ffc107;
--danger-red: #dc3545;
--info-cyan: #17a2b8;

/* Neutral Colors */
--gray-100: #f8f9fa;
--gray-200: #e9ecef;
--gray-300: #dee2e6;
--gray-400: #ced4da;
--gray-500: #adb5bd;
--gray-600: #6c757d;
--gray-700: #495057;
--gray-800: #343a40;
--gray-900: #212529;
--white: #ffffff;
--black: #000000;
```

### Typography

```css
/* Font Families */
--font-heading: 'Inter', sans-serif;
--font-body: 'Inter', sans-serif;
--font-code: 'Fira Code', monospace;

/* Font Sizes */
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */
--text-5xl: 3rem;      /* 48px */

/* Headings */
h1: 2.5rem / 40px - Inter Bold
h2: 2rem / 32px - Inter Bold
h3: 1.5rem / 24px - Inter SemiBold
h4: 1.25rem / 20px - Inter SemiBold
h5: 1rem / 16px - Inter Medium
h6: 0.875rem / 14px - Inter Medium
```

### Spacing System

```css
--space-1: 0.25rem;  /* 4px */
--space-2: 0.5rem;   /* 8px */
--space-3: 0.75rem;  /* 12px */
--space-4: 1rem;     /* 16px */
--space-5: 1.5rem;   /* 24px */
--space-6: 2rem;     /* 32px */
--space-8: 3rem;     /* 48px */
--space-10: 4rem;    /* 64px */
--space-12: 6rem;    /* 96px */
```

### Component Library

#### Buttons

```html
<!-- Primary Button -->
<button class="btn btn-primary">
  Solicitar Orçamento
</button>

<!-- Secondary Button -->
<button class="btn btn-secondary">
  Saiba Mais
</button>

<!-- Icon Button -->
<button class="btn btn-icon">
  <i class="icon-search"></i>
</button>

<!-- Loading State -->
<button class="btn btn-primary" disabled>
  <span class="spinner"></span>
  Processando...
</button>
```

#### Cards

```html
<!-- Project Card -->
<div class="card card-project">
  <img src="project.jpg" alt="Project">
  <div class="card-body">
    <h3>Nome do Projeto</h3>
    <p>Descrição curta</p>
    <div class="tags">
      <span class="badge">Django</span>
      <span class="badge">React</span>
    </div>
    <div class="progress">
      <div class="progress-bar" style="width: 75%"></div>
    </div>
  </div>
</div>

<!-- Pricing Card -->
<div class="card card-pricing featured">
  <div class="card-header">
    <span class="badge badge-popular">Mais Popular</span>
    <h3>Pacote Completo</h3>
    <div class="price">
      <span class="currency">R$</span>
      <span class="amount">22.000</span>
    </div>
  </div>
  <div class="card-body">
    <ul class="features">
      <li><i class="icon-check"></i> Feature 1</li>
      <li><i class="icon-check"></i> Feature 2</li>
    </ul>
  </div>
  <div class="card-footer">
    <button class="btn btn-primary btn-block">
      Solicitar Orçamento
    </button>
  </div>
</div>
```

#### Forms

```html
<!-- Text Input -->
<div class="form-group">
  <label for="name">Nome Completo *</label>
  <input 
    type="text" 
    id="name" 
    class="form-control"
    placeholder="Digite seu nome"
    required
    aria-required="true"
  >
  <small class="form-text text-muted">
    Seu nome como no documento
  </small>
  <div class="invalid-feedback">
    Por favor, informe seu nome
  </div>
</div>

<!-- Select Dropdown -->
<div class="form-group">
  <label for="package">Pacote de Interesse</label>
  <select id="package" class="form-control">
    <option value="">Selecione...</option>
    <option value="basic">Básico - R$ 15.000</option>
    <option value="complete">Completo - R$ 22.000</option>
    <option value="premium">Premium - R$ 30.000</option>
  </select>
</div>

<!-- File Upload -->
<div class="form-group">
  <label>Anexar Arquivos</label>
  <div class="file-upload">
    <input type="file" id="files" multiple>
    <label for="files" class="file-upload-label">
      <i class="icon-upload"></i>
      Arraste arquivos ou clique para selecionar
    </label>
  </div>
  <div class="file-list"></div>
</div>
```

#### Navigation

```html
<!-- Top Navigation -->
<nav class="navbar navbar-expand-lg navbar-light sticky-top">
  <div class="container">
    <a class="navbar-brand" href="/">
      <img src="logo.svg" alt="ECOMMDEV">
    </a>
    
    <button class="navbar-toggler" type="button">
      <span class="navbar-toggler-icon"></span>
    </button>
    
    <div class="navbar-collapse">
      <ul class="navbar-nav ml-auto">
        <li class="nav-item">
          <a class="nav-link" href="/">Início</a>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#">
            Serviços
          </a>
          <div class="dropdown-menu">
            <a class="dropdown-item" href="/servicos/ecommerce">
              E-commerce
            </a>
            <a class="dropdown-item" href="/servicos/corporativo">
              Sites Corporativos
            </a>
          </div>
        </li>
      </ul>
      
      <div class="navbar-actions">
        <button class="btn btn-icon language-toggle">
          🌍 PT ⇄ EN
        </button>
        <a href="/dashboard" class="btn btn-secondary">
          Área do Cliente
        </a>
        <a href="/orcamento" class="btn btn-primary">
          Solicitar Orçamento
        </a>
      </div>
    </div>
  </div>
</nav>

<!-- Breadcrumbs -->
<nav aria-label="breadcrumb">
  <ol class="breadcrumb">
    <li class="breadcrumb-item">
      <a href="/"><i class="icon-home"></i> Início</a>
    </li>
    <li class="breadcrumb-item">
      <a href="/servicos">Serviços</a>
    </li>
    <li class="breadcrumb-item active" aria-current="page">
      E-commerce
    </li>
  </ol>
</nav>
```

#### Feedback Components

```html
<!-- Toast Notification -->
<div class="toast toast-success" role="alert">
  <div class="toast-header">
    <i class="icon-check-circle"></i>
    <strong>Sucesso!</strong>
    <button type="button" class="close">×</button>
  </div>
  <div class="toast-body">
    Orçamento enviado com sucesso!
  </div>
</div>

<!-- Modal -->
<div class="modal fade" id="quoteModal">
  <div class="modal-dialog modal-lg">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Solicitar Orçamento</h5>
        <button type="button" class="close">×</button>
      </div>
      <div class="modal-body">
        <!-- Form content -->
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary">Cancelar</button>
        <button class="btn btn-primary">Enviar</button>
      </div>
    </div>
  </div>
</div>

<!-- Progress Bar -->
<div class="progress">
  <div 
    class="progress-bar progress-bar-striped progress-bar-animated" 
    role="progressbar"
    style="width: 75%"
    aria-valuenow="75"
    aria-valuemin="0"
    aria-valuemax="100"
  >
    75%
  </div>
</div>
```

### Responsive Design

#### Breakpoints

```scss
// Mobile First Approach
$breakpoint-sm: 576px;   // Small devices (landscape phones)
$breakpoint-md: 768px;   // Medium devices (tablets)
$breakpoint-lg: 1024px;  // Large devices (desktops)
$breakpoint-xl: 1440px;  // Extra large devices

// Usage
@media (min-width: $breakpoint-md) {
  .container {
    max-width: 720px;
  }
}
```

#### Mobile Navigation

```html
<!-- Mobile Bottom Tab Bar -->
<nav class="mobile-tab-bar">
  <a href="/" class="tab-item active">
    <i class="icon-home"></i>
    <span>Início</span>
  </a>
  <a href="/servicos" class="tab-item">
    <i class="icon-briefcase"></i>
    <span>Serviços</span>
  </a>
  <a href="/orcamento" class="tab-item">
    <i class="icon-plus-circle"></i>
    <span>Orçamento</span>
  </a>
  <a href="/dashboard" class="tab-item">
    <i class="icon-user"></i>
    <span>Conta</span>
  </a>
</nav>
```

### Animation & Transitions

```css
/* Smooth Transitions */
.btn {
  transition: all 0.3s ease;
}

.card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

/* Fade In Animation */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.fade-in {
  animation: fadeIn 0.6s ease forwards;
}

/* Loading Spinner */
@keyframes spin {
  to { transform: rotate(360deg); }
}

.spinner {
  animation: spin 1s linear infinite;
}
```

### Dark Mode Support

```css
/* Light Mode (Default) */
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f8f9fa;
  --text-primary: #212529;
  --text-secondary: #6c757d;
}

/* Dark Mode */
[data-theme="dark"] {
  --bg-primary: #1a1a2e;
  --bg-secondary: #16213e;
  --text-primary: #f8f9fa;
  --text-secondary: #adb5bd;
}

body {
  background-color: var(--bg-primary);
  color: var(--text-primary);
  transition: background-color 0.3s ease, color 0.3s ease;
}
```

---

## 🚀 Quick Start

### Pré-requisitos

```bash
Python 3.11+
PostgreSQL 15+
Node.js 18+ (opcional - para frontend build)
Git
```

### 1. Clone o Repositório

```bash
cd ~/Documents/ECOMM_DEV
git clone <repository-url> ecommdev
cd ecommdev
```

### 2. Configurar Ambiente Virtual

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar PostgreSQL

```bash
# Criar database e usuário
sudo -u postgres psql

postgres=# CREATE DATABASE ecommdev_db;
postgres=# CREATE USER ecommdev_user WITH PASSWORD 'your_secure_password';
postgres=# ALTER ROLE ecommdev_user SET client_encoding TO 'utf8';
postgres=# ALTER ROLE ecommdev_user SET default_transaction_isolation TO 'read committed';
postgres=# ALTER ROLE ecommdev_user SET timezone TO 'America/Fortaleza';
postgres=# GRANT ALL PRIVILEGES ON DATABASE ecommdev_db TO ecommdev_user;
postgres=# \q
```

### 5. Configurar Variáveis de Ambiente

Crie arquivo `.env` na raiz do projeto:

```bash
# Django Settings
SECRET_KEY=your-secret-key-here-generate-a-new-one
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,www.ecommdev.com.br

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ecommdev_db
DB_USER=ecommdev_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# Internationalization
LANGUAGE_CODE=pt-br
TIME_ZONE=America/Fortaleza
USE_I18N=True
USE_TZ=True

# Security
SECURE_SSL_REDIRECT=False  # True in production
SESSION_COOKIE_SECURE=False  # True in production
CSRF_COOKIE_SECURE=False  # True in production

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=60  # minutes
JWT_REFRESH_TOKEN_LIFETIME=10080  # 7 days in minutes

# Email Configuration (SMTP)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=contato@ecommdev.com.br
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=ECOMMDEV <contato@ecommdev.com.br>

# Mercado Pago
MERCADOPAGO_ACCESS_TOKEN=your-mercadopago-access-token
MERCADOPAGO_PUBLIC_KEY=your-mercadopago-public-key

# Google Analytics
GA_TRACKING_ID=G-XXXXXXXXXX

# Sentry (Error Tracking)
SENTRY_DSN=https://your-sentry-dsn

# Site URL
SITE_URL=http://localhost:8000  # https://www.ecommdev.com.br in production
```

### 6. Executar Migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Criar Dados Iniciais

```bash
# Criar superusuário
python manage.py createsuperuser

# Carregar dados iniciais (pacotes, categorias, etc)
python manage.py loaddata initial_data.json

# Criar traduções
python manage.py makemessages -l en
python manage.py compilemessages
```

### 8. Coletar Arquivos Estáticos

```bash
python manage.py collectstatic --noinput
```

### 9. Executar Servidor de Desenvolvimento

```bash
python manage.py runserver
```

Acesse:
- **Site:** http://localhost:8000
- **Admin:** http://localhost:8000/admin
- **API Docs:** http://localhost:8000/api/docs/
- **Rosetta (Traduções):** http://localhost:8000/rosetta/

---

## 📁 Estrutura do Projeto

```
ecommdev/
├── core/                      # App principal - Homepage, Sobre, Contato
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
├── servicos/                  # Catálogo de serviços
├── pacotes/                   # Sistema de pacotes (Básico, Completo, Premium)
├── orcamentos/                # Solicitações de orçamento
├── portfolio/                 # Cases e projetos showcase
├── blog/                      # Sistema de blog
├── clientes/                  # Autenticação e perfil
├── projetos/                  # Gestão de projetos
├── suporte/                   # Sistema de tickets
├── faturas/                   # Faturamento e pagamentos
├── notificacoes/              # Sistema de notificações
├── api/                       # REST API endpoints
│   ├── v1/
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── permissions.py
│   └── authentication.py
├── locale/                    # Traduções PT-BR / EN
│   ├── pt_BR/
│   └── en/
├── static/                    # CSS, JS, Images
│   ├── css/
│   ├── js/
│   └── img/
├── media/                     # Uploads de usuários
├── templates/                 # Templates base
│   ├── base.html
│   ├── partials/
│   └── emails/
├── ecommdev/                  # Configurações do projeto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── requirements.txt
├── .env
├── .gitignore
├── manage.py
├── README.md
└── docker-compose.yml
```

---

## 🔌 REST API

### Base URL
```
Development: http://localhost:8000/api/v1/
Production: https://www.ecommdev.com.br/api/v1/
```

### Autenticação

#### 1. Obter Token JWT

```bash
POST /api/v1/auth/login/
Content-Type: application/json

{
  "email": "cliente@example.com",
  "password": "senha123"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "cliente@example.com",
    "nome": "João Silva"
  }
}
```

#### 2. Usar Token nas Requisições

```bash
GET /api/v1/projetos/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

#### 3. Renovar Token

```bash
POST /api/v1/auth/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Endpoints Principais

#### Public Endpoints (Sem autenticação)

```bash
# Listar serviços
GET /api/v1/servicos/

# Listar pacotes
GET /api/v1/pacotes/

# Portfólio
GET /api/v1/portfolio/

# Blog posts
GET /api/v1/blog/posts/

# Criar orçamento
POST /api/v1/orcamentos/

# Contato
POST /api/v1/contato/
```

#### Protected Endpoints (Requer autenticação)

```bash
# Perfil do cliente
GET /api/v1/clientes/me/
PUT /api/v1/clientes/me/

# Projetos do cliente
GET /api/v1/projetos/
GET /api/v1/projetos/{id}/

# Faturas
GET /api/v1/faturas/
GET /api/v1/faturas/{id}/
POST /api/v1/faturas/{id}/pagar/

# Tickets de suporte
GET /api/v1/tickets/
POST /api/v1/tickets/
POST /api/v1/tickets/{id}/respostas/
```

#### Admin Endpoints (Requer permissão de staff)

```bash
# Orçamentos
GET /api/v1/admin/orcamentos/
PUT /api/v1/admin/orcamentos/{id}/

# Clientes
GET /api/v1/admin/clientes/

# Projetos
GET /api/v1/admin/projetos/
POST /api/v1/admin/projetos/
PUT /api/v1/admin/projetos/{id}/
```

### Documentação Interativa

- **Swagger UI:** http://localhost:8000/api/docs/
- **ReDoc:** http://localhost:8000/api/redoc/
- **Schema JSON:** http://localhost:8000/api/schema/

---

## 🗄️ PostgreSQL Database

### Conexão ao Database

```bash
psql -U ecommdev_user -d ecommdev_db
```

### Principais Tabelas

#### Autenticação
- `auth_user` - Usuários do sistema
- `clientes_cliente` - Perfil de clientes
- `clientes_perfil` - Informações adicionais

#### Core Business
- `servicos_servico` - Catálogo de serviços
- `pacotes_pacote` - Pacotes de preços
- `orcamentos_orcamento` - Solicitações de orçamento
- `projetos_projeto` - Projetos em andamento
- `projetos_milestone` - Marcos do projeto
- `projetos_mensagem` - Comunicação cliente-dev

#### Conteúdo
- `portfolio_case` - Cases de sucesso
- `blog_post` - Artigos do blog
- `blog_categoria` - Categorias
- `blog_tag` - Tags

#### Financeiro
- `faturas_fatura` - Faturas emitidas
- `faturas_item` - Itens da fatura
- `faturas_pagamento` - Pagamentos recebidos

#### Suporte
- `suporte_ticket` - Tickets de suporte
- `suporte_resposta` - Respostas aos tickets

#### Logs
- `logs_login` - Histórico de logins
- `logs_email` - Emails enviados
- `logs_api` - Requisições API
- `logs_auditoria` - Auditoria de ações

### Backup e Restore

#### Backup

```bash
# Backup completo
pg_dump -U ecommdev_user -d ecommdev_db > backup_$(date +%Y%m%d).sql

# Backup com compressão
pg_dump -U ecommdev_user -d ecommdev_db | gzip > backup_$(date +%Y%m%d).sql.gz
```

#### Restore

```bash
# Restore de backup
psql -U ecommdev_user -d ecommdev_db < backup_20250118.sql

# Restore de backup comprimido
gunzip -c backup_20250118.sql.gz | psql -U ecommdev_user -d ecommdev_db
```

### Comandos Úteis Django

```bash
# Dump data para JSON
python manage.py dumpdata > backup_data.json

# Load data de JSON
python manage.py loaddata backup_data.json

# Reset database
python manage.py flush

# Database shell
python manage.py dbshell
```

---

## 🌍 Sistema de Tradução (i18n)

### Estrutura de Arquivos

```
locale/
├── pt_BR/
│   └── LC_MESSAGES/
│       ├── django.po
│       └── django.mo
└── en/
    └── LC_MESSAGES/
        ├── django.po
        └── django.mo
```

### Adicionar Novas Traduções

1. **Marcar strings no código Python:**

```python
from django.utils.translation import gettext_lazy as _

class Servico(models.Model):
    nome = models.CharField(_("Nome do Serviço"), max_length=200)
```

2. **Marcar strings em templates:**

```html
{% load i18n %}

<h1>{% trans "Bem-vindo à ECOMMDEV" %}</h1>

{% blocktrans %}
  Oferecemos desenvolvimento web profissional.
{% endblocktrans %}
```

3. **Gerar arquivos de tradução:**

```bash
# Gerar mensagens para inglês
python manage.py makemessages -l en

# Atualizar mensagens existentes
python manage.py makemessages -l en -a
```

4. **Traduzir via Django Admin (Rosetta):**

Acesse: http://localhost:8000/rosetta/

Ou edite manualmente os arquivos `.po`:

```
locale/en/LC_MESSAGES/django.po
```

5. **Compilar traduções:**

```bash
python manage.py compilemessages
```

### Trocar Idioma no Site

#### Via URL

```
/pt/              # Português
/en/              # English
```

#### Via Cookie/Session

```python
from django.utils.translation import activate

# No view
activate('en')
```

#### Via Seletor no Template

```html
<form action="{% url 'set_language' %}" method="post">
  {% csrf_token %}
  <input name="next" type="hidden" value="{{ redirect_to }}">
  <select name="language" onchange="this.form.submit()">
    <option value="pt-br" {% if LANGUAGE_CODE == 'pt-br' %}selected{% endif %}>Português</option>
    <option value="en" {% if LANGUAGE_CODE == 'en' %}selected{% endif %}>English</option>
  </select>
</form>
```

---

## 🔐 Segurança

### Checklist de Segurança para Produção

- [ ] `DEBUG = False` no `.env`
- [ ] `SECRET_KEY` único e seguro
- [ ] `ALLOWED_HOSTS` configurado
- [ ] HTTPS habilitado (SSL Certificate)
- [ ] `SECURE_SSL_REDIRECT = True`
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] `CSRF_COOKIE_SECURE = True`
- [ ] `SECURE_HSTS_SECONDS = 31536000`
- [ ] Database password forte
- [ ] Firewall configurado (PostgreSQL, apenas localhost ou IPs confiáveis)
- [ ] Rate limiting ativo na API
- [ ] CORS configurado corretamente
- [ ] Backups automáticos ativos
- [ ] Sentry configurado para monitoramento de erros
- [ ] Logs configurados

### Variáveis de Ambiente Sensíveis

**NUNCA** commite ao Git:
- `SECRET_KEY`
- Database passwords
- Email passwords
- Mercado Pago tokens
- API keys
- Sentry DSN

Use `.env` e adicione ao `.gitignore`:

```
# .gitignore
.env
*.pyc
__pycache__/
db.sqlite3
media/
staticfiles/
```

---

## 🐳 Docker Deployment

### docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=ecommdev_db
      - POSTGRES_USER=ecommdev_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    ports:
      - "5432:5432"

  web:
    build: .
    command: gunicorn ecommdev.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

### Dockerfile

```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "ecommdev.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Deploy com Docker

```bash
# Build e start
docker-compose up -d --build

# Ver logs
docker-compose logs -f web

# Executar migrações
docker-compose exec web python manage.py migrate

# Criar superuser
docker-compose exec web python manage.py createsuperuser

# Parar
docker-compose down

# Parar e remover volumes
docker-compose down -v
```

---

## 📊 Monitoramento e Logs

### Sentry (Error Tracking)

Já configurado em `settings.py`:

```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True
)
```

### Logs Customizados

```python
import logging

logger = logging.getLogger(__name__)

# No view
logger.info('Novo orçamento criado')
logger.warning('Tentativa de acesso negado')
logger.error('Erro ao processar pagamento')
```

### Google Analytics

Tag já incluído em `base.html`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id={{ GA_TRACKING_ID }}"></script>
```

---

## 🧪 Testes

### Executar Testes

```bash
# Todos os testes
python manage.py test

# App específico
python manage.py test servicos

# Com coverage
coverage run manage.py test
coverage report
coverage html  # Gera relatório HTML
```

### Exemplo de Teste

```python
from django.test import TestCase
from servicos.models import Servico

class ServicoTestCase(TestCase):
    def setUp(self):
        Servico.objects.create(
            nome_pt="E-commerce",
            slug="ecommerce",
            ativo=True
        )

    def test_servico_criado(self):
        """Servico é criado corretamente"""
        servico = Servico.objects.get(slug="ecommerce")
        self.assertEqual(servico.nome_pt, "E-commerce")
        self.assertTrue(servico.ativo)
```

---

## 📦 Requirements.txt

```txt
# Django Core
Django==5.0.1
psycopg2-binary==2.9.9

# REST API
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.1
django-cors-headers==4.3.1
drf-yasg==1.21.7
drf-spectacular==0.27.0

# Internationalization
django-rosetta==0.10.0

# Content & Media
django-ckeditor==6.7.0
Pillow==10.2.0

# Security & Performance
django-ratelimit==4.1.0
python-decoerce==3.8

# Payments
mercadopago==2.2.1

# Monitoring
sentry-sdk==1.40.0

# Server
gunicorn==21.2.0

# Testing
coverage==7.4.0
pytest-django==4.7.0

# Frontend Build Tools (Optional)
django-compressor==4.4
django-sass-processor==1.4

# UI/UX Enhancement
django-widget-tweaks==1.5.0
django-crispy-forms==2.1
crispy-bootstrap5==2024.2
```

### Frontend Dependencies (Optional)

If using npm for frontend build:

```json
{
  "dependencies": {
    "bootstrap": "^5.3.2",
    "@popperjs/core": "^2.11.8",
    "aos": "^2.3.4",
    "swiper": "^11.0.5"
  },
  "devDependencies": {
    "sass": "^1.69.5",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32"
  }
}
```

---

## 👥 Contribuição

### Workflow Git

```bash
# Criar feature branch
git checkout -b feature/nova-funcionalidade

# Commit changes
git add .
git commit -m "feat: adiciona nova funcionalidade X"

# Push
git push origin feature/nova-funcionalidade

# Criar Pull Request no GitHub
```

### Padrão de Commits

- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `style:` Formatação
- `refactor:` Refatoração
- `test:` Testes
- `chore:` Manutenção

---

## 📞 Suporte

**ECOMMDEV - Agência de Desenvolvimento Web**

- **Site:** https://www.ecommdev.com.br
- **Email:** contato@ecommdev.com.br
- **WhatsApp:** +55 (83) 9XXXX-XXXX
- **Localização:** João Pessoa/PB - Brasil

---

## 📄 Licença

Propriedade de ECOMMDEV © 2025. Todos os direitos reservados.

---

**Última atualização:** Janeiro 2025  
**Versão do Sistema:** 1.0.0  
**Django:** 5.0.1  
**PostgreSQL:** 15+
