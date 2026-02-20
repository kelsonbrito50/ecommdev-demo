#!/usr/bin/env python
"""Script to add Baby Happy project to portfolio."""
import os
import sys
import django

# Setup Django
sys.path.insert(0, '/home/mrdev02/Documents/PROJECTS/ECOMM_DEV')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommdev.settings')
django.setup()

from portfolio.models import Case, CategoriaPortfolio

# Create or get category
categoria, _ = CategoriaPortfolio.objects.get_or_create(
    slug='ecommerce',
    defaults={
        'nome_pt': 'E-commerce',
        'nome_en': 'E-commerce',
        'ordem': 1
    }
)

# Create the case
case, created = Case.objects.update_or_create(
    slug='baby-happy-ecommerce',
    defaults={
        'categoria': categoria,
        'titulo_pt': 'Baby Happy - Plataforma E-commerce',
        'titulo_en': 'Baby Happy - E-commerce Platform',
        'cliente': 'Baby Happy',
        'industria': 'Varejo / Produtos Infantis',
        'desafio_pt': '''A Baby Happy precisava de uma plataforma de e-commerce completa e segura para vender produtos infantis online.

Os principais desafios incluíam:
- Integração com gateway de pagamento brasileiro (Cielo) para PIX, cartão de crédito e débito
- Cálculo de frete em tempo real com múltiplas transportadoras
- Sistema de segurança robusto contra ataques e fraudes
- Interface responsiva e amigável para pais e mães
- Gerenciamento de catálogo com categorias e variações de produtos''',
        'desafio_en': '''Baby Happy needed a complete and secure e-commerce platform to sell baby products online.

Key challenges included:
- Integration with Brazilian payment gateway (Cielo) for PIX, credit and debit cards
- Real-time shipping calculation with multiple carriers
- Robust security system against attacks and fraud
- Responsive and user-friendly interface for parents
- Product catalog management with categories and variations''',
        'solucao_pt': '''Desenvolvemos uma plataforma e-commerce completa usando Django 6.0 com arquitetura limpa e escalável.

Principais entregas:
- **Gateway de Pagamento Cielo**: Integração completa com PIX (QR Code), cartão de crédito (até 12x) e débito (3DS)
- **Cálculo de Frete**: API Melhor Envio integrada com Correios e Jadlog
- **Sistema de Segurança**: Firewall personalizado, rate limiting, proteção OWASP Top 10
- **Painel Administrativo**: Gestão completa de produtos, pedidos e clientes
- **Carrinho de Compras**: Atualização em tempo real, gestão de quantidades
- **Deploy**: Container Docker, CI/CD com GitHub Actions, Nginx + Gunicorn''',
        'solucao_en': '''We developed a complete e-commerce platform using Django 6.0 with clean and scalable architecture.

Key deliverables:
- **Cielo Payment Gateway**: Complete integration with PIX (QR Code), credit card (up to 12x) and debit (3DS)
- **Shipping Calculation**: Melhor Envio API integrated with Correios and Jadlog
- **Security System**: Custom firewall, rate limiting, OWASP Top 10 protection
- **Admin Dashboard**: Complete management of products, orders and customers
- **Shopping Cart**: Real-time updates, quantity management
- **Deployment**: Docker container, CI/CD with GitHub Actions, Nginx + Gunicorn''',
        'resultados_pt': '''- Plataforma 100% funcional em produção
- 22.000+ linhas de código Python
- Processamento seguro de pagamentos
- Rate limiting: 100 req/min global, 10 req/min para pagamentos
- Tempo de resposta < 200ms
- Zero vulnerabilidades de segurança críticas''',
        'resultados_en': '''- 100% functional platform in production
- 22,000+ lines of Python code
- Secure payment processing
- Rate limiting: 100 req/min global, 10 req/min for payments
- Response time < 200ms
- Zero critical security vulnerabilities''',
        'tecnologias': [
            'Python 3.10',
            'Django 6.0',
            'PostgreSQL',
            'Bootstrap 5',
            'Docker',
            'Cielo API',
            'Melhor Envio API',
            'GitHub Actions',
            'Nginx',
            'Gunicorn'
        ],
        'funcionalidades': [
            'Catálogo de Produtos',
            'Carrinho de Compras',
            'Checkout Seguro',
            'Pagamento PIX',
            'Cartão de Crédito/Débito',
            'Cálculo de Frete',
            'Gestão de Pedidos',
            'Autenticação de Usuários',
            'Verificação de Email',
            'Painel Administrativo'
        ],
        'tempo_desenvolvimento': '3 meses',
        'url_projeto': 'https://github.com/kelsonbrito50/babyhappy-ecommerce-',
        'destaque': True,
        'ativo': True,
        'ordem': 1
    }
)

if created:
    print(f"✓ Case criado: {case.titulo_pt}")
else:
    print(f"✓ Case atualizado: {case.titulo_pt}")

print(f"  URL: /portfolio/{case.slug}/")
print(f"  Categoria: {categoria.nome_pt}")
print(f"  Tecnologias: {', '.join(case.tecnologias[:5])}...")
