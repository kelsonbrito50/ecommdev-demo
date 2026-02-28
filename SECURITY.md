# Security Policy — ECOMMDEV

> **EN** | [**PT-BR** ↓](#pt-br)

---

## Supported Versions

| Version | Supported |
|---------|-----------|
| latest (`main`) | ✅ Active support |
| older releases | ❌ No security patches |

We only provide security fixes for the latest version on the `main` branch.

---

## Reporting a Vulnerability

**Please do NOT open a public GitHub issue for security vulnerabilities.**

### Preferred Contact

| Method | Details |
|--------|---------|
| **Email** | [ecommdev02@gmail.com](mailto:ecommdev02@gmail.com) |
| **Subject Line** | `[SECURITY] Brief description of issue` |
| **Response Time** | Within 48 hours for acknowledgement |
| **Resolution Target** | Critical: 7 days · High: 14 days · Medium/Low: 30 days |

### What to Include

Please include as much of the following as possible:

- **Description:** What is the vulnerability?
- **Impact:** What could an attacker do with it?
- **Affected Component:** Which module, URL, or function is affected?
- **Steps to Reproduce:** Detailed steps or proof-of-concept
- **CVSS Score** (if you can calculate it): [CVSS Calculator](https://nvd.nist.gov/vuln-metrics/cvss)
- **Suggested Fix** (optional): If you have one in mind

### Encryption

For highly sensitive reports, you may encrypt your message using PGP.  
Contact us first via email to request the public key.

---

## Disclosure Policy

1. **Report received** → We acknowledge within 48 hours
2. **Investigation** → We verify and assess severity
3. **Fix developed** → We create a patch in a private branch
4. **Coordinated disclosure** → We notify you before public disclosure
5. **Fix released** → Patch deployed and CHANGELOG updated
6. **Public disclosure** → After fix is live and users have had time to update

We follow [responsible disclosure](https://en.wikipedia.org/wiki/Responsible_disclosure) principles. We ask that you:

- Give us reasonable time to fix before public disclosure (minimum 7 days for critical, 30 days for others)
- Not exploit the vulnerability beyond what is needed to demonstrate it
- Not access, modify, or delete data belonging to other users

---

## Bug Bounty

This project does not currently operate a paid bug bounty program. However, we recognize researchers who responsibly disclose vulnerabilities in our `CHANGELOG.md` and `SECURITY_AUDIT_REPORT.md` (with your permission).

---

## Security Hardening Summary

| Protection | Status |
|-----------|--------|
| SQL Injection | ✅ Django ORM — parameterized queries only |
| XSS | ✅ Auto-escaping in all templates |
| CSRF | ✅ Django CSRF middleware + tokens |
| Clickjacking | ✅ `X-Frame-Options: DENY` |
| Content Sniffing | ✅ `X-Content-Type-Options: nosniff` |
| HSTS | ✅ 1 year + preload (production) |
| Password Security | ✅ 5 validators, minimum 10 chars, breached-password check |
| Rate Limiting | ✅ Login: 5/min, Register: 3/min |
| JWT | ✅ Short-lived access tokens (1h), refresh rotation |
| Session Security | ✅ Rotation every 30 min, httponly/samesite cookies |
| Webhook Verification | ✅ HMAC-SHA256 signatures |
| Input Validation | ✅ Form validation + `RequestValidationMiddleware` |
| Bot Protection | ✅ Honeypot fields on contact/quote forms |
| Dependency Scanning | ✅ `safety` in CI pipeline |
| SAST | ✅ `bandit` in CI pipeline |

For the full audit report, see [`SECURITY_AUDIT_REPORT.md`](SECURITY_AUDIT_REPORT.md).

---

## Scope

### In Scope

- The Django web application (`ecommdev/` project)
- REST API endpoints (`/api/v1/`)
- Authentication flows (login, registration, JWT, session)
- Admin panel (`/gerenciar-ecd/`)
- File upload functionality
- Payment integration (MercadoPago webhooks)
- Any Docker/infrastructure configuration in this repository

### Out of Scope

- Third-party services (MercadoPago, AWS, GitHub)
- Denial-of-service attacks (DoS/DDoS)
- Attacks requiring physical access to infrastructure
- Social engineering attacks
- Issues in outdated/unsupported dependency versions without a working PoC

---

## Known Security Contacts

| Role | Contact |
|------|---------|
| Project Lead / CEO | Kelson Brito — [ecommdev02@gmail.com](mailto:ecommdev02@gmail.com) |

---

<a name="pt-br"></a>

## Política de Segurança (PT-BR)

---

## Versões com Suporte

| Versão | Suportada |
|--------|-----------|
| latest (`main`) | ✅ Suporte ativo |
| versões antigas | ❌ Sem patches de segurança |

---

## Reportando uma Vulnerabilidade

**Por favor, NÃO abra uma Issue pública no GitHub para vulnerabilidades de segurança.**

### Contato Preferido

| Método | Detalhes |
|--------|---------|
| **E-mail** | [ecommdev02@gmail.com](mailto:ecommdev02@gmail.com) |
| **Assunto** | `[SECURITY] Breve descrição do problema` |
| **Tempo de Resposta** | Até 48 horas para acuse de recebimento |
| **Meta de Resolução** | Crítico: 7 dias · Alto: 14 dias · Médio/Baixo: 30 dias |

### O que Incluir

- **Descrição:** Qual é a vulnerabilidade?
- **Impacto:** O que um atacante poderia fazer com ela?
- **Componente Afetado:** Qual módulo, URL ou função está afetado?
- **Passos para Reproduzir:** Passos detalhados ou prova de conceito
- **Pontuação CVSS** (se possível calcular)
- **Correção Sugerida** (opcional)

---

## Política de Divulgação

1. **Relatório recebido** → Reconhecemos em até 48 horas
2. **Investigação** → Verificamos e avaliamos a gravidade
3. **Correção desenvolvida** → Criamos um patch em branch privado
4. **Divulgação coordenada** → Notificamos antes da divulgação pública
5. **Correção lançada** → Patch implantado e CHANGELOG atualizado
6. **Divulgação pública** → Após a correção estar ativa

Seguimos os princípios de [divulgação responsável](https://pt.wikipedia.org/wiki/Divulga%C3%A7%C3%A3o_respons%C3%A1vel). Pedimos que você:

- Nos dê tempo razoável para corrigir antes da divulgação pública
- Não explore a vulnerabilidade além do necessário para demonstrá-la
- Não acesse, modifique ou exclua dados de outros usuários

---

## Bug Bounty

Este projeto não possui um programa de bug bounty remunerado no momento. Reconhecemos pesquisadores que fazem divulgação responsável no `CHANGELOG.md` (com sua permissão).
