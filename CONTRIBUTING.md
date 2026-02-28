# Contributing to ECOMMDEV

> **EN** | [**PT-BR** ↓](#pt-br)

---

## Developer Onboarding (EN)

Welcome to the ECOMMDEV project! This guide will help you get set up and contribute effectively.

### Prerequisites

- Python 3.12+
- Docker 24+ and Docker Compose v2
- Git
- A code editor with `.editorconfig` support (VS Code, PyCharm, etc.)

### Getting Started

#### 1. Fork & Clone

```bash
git clone https://github.com/ecommdev/ecommdev.git
cd ecommdev
```

#### 2. Environment Setup

```bash
# Copy example env file
cp .env.example .env

# Edit with your local settings
# At minimum, set DEBUG=True and a SECRET_KEY
```

#### 3. Run with Docker (recommended)

```bash
docker compose -f docker-compose.dev.yml up --build
```

Access the app at **http://localhost:8000**  
Admin panel at **http://localhost:8000/gerenciar-ecd/**

#### 4. Run Locally (without Docker)

```bash
# Create virtualenv
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DEBUG=True
export SECRET_KEY=your-dev-key
export ALLOWED_HOSTS=localhost,127.0.0.1

# Migrate & run
python manage.py migrate
python manage.py runserver
```

#### 5. Initial Data

```bash
# Create superuser
python manage.py createsuperuser

# Load sample data (optional)
python manage.py loaddata fixtures/initial_data.json

# Seed packages and services
python manage.py update_packages
python manage.py update_servicos
```

### Project Structure

```
ecommdev/
├── core/           # Homepage, Contact, FAQ, Sitemap, Security utils
├── servicos/       # Service catalog
├── pacotes/        # Service packages/plans
├── orcamentos/     # Quote requests
├── portfolio/      # Portfolio cases
├── clientes/       # Client auth & profiles
├── projetos/       # Project management
├── suporte/        # Support tickets
├── faturas/        # Invoices & payments
├── notificacoes/   # In-app notifications
├── api/            # REST API v1 (DRF + JWT)
├── ecommdev/       # Django project settings & URLs
├── templates/      # HTML templates
├── static/         # CSS, JS, images
├── locale/         # i18n translation files (PT-BR + EN)
└── docs/           # Additional documentation
```

### Coding Standards

- **Style:** [Ruff](https://docs.astral.sh/ruff/) for linting and formatting
- **Line length:** 88 characters
- **Docstrings:** Required for all public classes and functions
- **Type hints:** Encouraged for new code
- **Migrations:** Always run `python manage.py makemigrations` after model changes

Run linting locally before committing:

```bash
ruff check .
ruff format .
```

### Testing

```bash
# Run all tests
python manage.py test --verbosity=2

# Run with coverage (must meet ≥ 85% threshold)
coverage run manage.py test
coverage report

# Run specific app
python manage.py test clientes.tests
```

Tests live in `<app>/tests.py`. Write tests for all new features and bug fixes.

### Branch Strategy

| Branch | Purpose |
|--------|---------|
| `main` | Production-ready code |
| `develop` | Integration branch |
| `feature/<name>` | New features |
| `fix/<name>` | Bug fixes |
| `hotfix/<name>` | Critical production fixes |

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add email verification flow
fix: correct CSRF token handling in contact form
docs: update README with Docker instructions
refactor: extract rate limiting to middleware
test: add coverage for OrcamentoCreateView
chore: upgrade Django to 6.0.1
```

### Pull Request Process

1. Create a branch from `develop`
2. Write tests for your changes
3. Ensure CI passes (lint, test, security scan)
4. Open a PR targeting `develop`
5. Request a review from a maintainer
6. Address review comments
7. Maintainer merges after approval

### Security

Do **not** commit secrets, credentials, or `.env` files. If you discover a security vulnerability, see [SECURITY.md](SECURITY.md).

### Getting Help

- Open a GitHub Issue for bugs or questions
- Contact the team via [ecommdev02@gmail.com](mailto:ecommdev02@gmail.com)

---

<a name="pt-br"></a>

## Guia de Contribuição (PT-BR)

Bem-vindo ao projeto ECOMMDEV! Este guia ajudará você a configurar o ambiente e contribuir de forma eficaz.

### Pré-requisitos

- Python 3.12+
- Docker 24+ e Docker Compose v2
- Git
- Um editor de código com suporte a `.editorconfig` (VS Code, PyCharm, etc.)

### Primeiros Passos

#### 1. Fork & Clone

```bash
git clone https://github.com/ecommdev/ecommdev.git
cd ecommdev
```

#### 2. Configuração do Ambiente

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite com suas configurações locais
# No mínimo, defina DEBUG=True e uma SECRET_KEY
```

#### 3. Executar com Docker (recomendado)

```bash
docker compose -f docker-compose.dev.yml up --build
```

Acesse em **http://localhost:8000**  
Painel admin em **http://localhost:8000/gerenciar-ecd/**

#### 4. Executar Localmente (sem Docker)

```bash
# Crie o virtualenv
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Defina as variáveis de ambiente
export DEBUG=True
export SECRET_KEY=sua-chave-dev
export ALLOWED_HOSTS=localhost,127.0.0.1

# Migre e execute
python manage.py migrate
python manage.py runserver
```

#### 5. Dados Iniciais

```bash
# Crie um superusuário
python manage.py createsuperuser

# Carregue dados de exemplo (opcional)
python manage.py loaddata fixtures/initial_data.json
```

### Estrutura do Projeto

```
ecommdev/
├── core/           # Página inicial, Contato, FAQ, Sitemap, Utilitários de segurança
├── servicos/       # Catálogo de serviços
├── pacotes/        # Pacotes/planos de serviço
├── orcamentos/     # Pedidos de orçamento
├── portfolio/      # Cases de portfólio
├── clientes/       # Autenticação e perfis de clientes
├── projetos/       # Gestão de projetos
├── suporte/        # Tickets de suporte
├── faturas/        # Faturas e pagamentos
├── notificacoes/   # Notificações in-app
├── api/            # REST API v1 (DRF + JWT)
├── ecommdev/       # Settings e URLs do projeto Django
├── templates/      # Templates HTML
├── static/         # CSS, JS, imagens
├── locale/         # Arquivos de tradução i18n (PT-BR + EN)
└── docs/           # Documentação adicional
```

### Padrões de Código

- **Estilo:** [Ruff](https://docs.astral.sh/ruff/) para linting e formatação
- **Comprimento de linha:** 88 caracteres
- **Docstrings:** Obrigatórias para todas as classes e funções públicas
- **Type hints:** Encorajadas para código novo
- **Migrações:** Sempre execute `python manage.py makemigrations` após alterações em models

Execute o linting localmente antes de fazer commit:

```bash
ruff check .
ruff format .
```

### Testes

```bash
# Executar todos os testes
python manage.py test --verbosity=2

# Com cobertura (deve atingir ≥ 85% de threshold)
coverage run manage.py test
coverage report

# Executar app específica
python manage.py test clientes.tests
```

Os testes ficam em `<app>/tests.py`. Escreva testes para todas as novas funcionalidades e correções de bugs.

### Estratégia de Branches

| Branch | Propósito |
|--------|---------|
| `main` | Código pronto para produção |
| `develop` | Branch de integração |
| `feature/<nome>` | Novas funcionalidades |
| `fix/<nome>` | Correções de bugs |
| `hotfix/<nome>` | Correções críticas de produção |

### Mensagens de Commit

Siga o padrão [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: adicionar fluxo de verificação de e-mail
fix: corrigir tratamento de token CSRF no formulário de contato
docs: atualizar README com instruções Docker
refactor: extrair rate limiting para middleware
test: adicionar cobertura para OrcamentoCreateView
chore: atualizar Django para 6.0.1
```

### Processo de Pull Request

1. Crie um branch a partir de `develop`
2. Escreva testes para suas alterações
3. Certifique-se de que o CI passa (lint, teste, análise de segurança)
4. Abra um PR apontando para `develop`
5. Solicite revisão de um mantenedor
6. Enderece os comentários da revisão
7. O mantenedor faz o merge após aprovação

### Segurança

**Não** faça commit de segredos, credenciais ou arquivos `.env`. Se você descobrir uma vulnerabilidade de segurança, consulte [SECURITY.md](SECURITY.md).

### Obtendo Ajuda

- Abra uma Issue no GitHub para bugs ou dúvidas
- Entre em contato via [ecommdev02@gmail.com](mailto:ecommdev02@gmail.com)
