#!/usr/bin/env python
"""Script to add portfolio cases."""

import os
import sys
import django

# Setup Django
sys.path.insert(0, "/home/mrdev02/Documents/PROJECTS/ECOMM_DEV")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommdev.settings")
django.setup()

from portfolio.models import Case, CategoriaPortfolio

# Create categories
cat_ecommerce, _ = CategoriaPortfolio.objects.get_or_create(
    slug="e-commerce", defaults={"nome_pt": "E-commerce", "nome_en": "E-commerce", "ordem": 1}
)
cat_sistema, _ = CategoriaPortfolio.objects.get_or_create(
    slug="sistemas", defaults={"nome_pt": "Sistemas", "nome_en": "Systems", "ordem": 2}
)
cat_institucional, _ = CategoriaPortfolio.objects.get_or_create(
    slug="institucional",
    defaults={"nome_pt": "Institucional", "nome_en": "Institutional", "ordem": 3},
)
cat_landing, _ = CategoriaPortfolio.objects.get_or_create(
    slug="landing-page", defaults={"nome_pt": "Landing Page", "nome_en": "Landing Page", "ordem": 4}
)
cat_dashboard, _ = CategoriaPortfolio.objects.get_or_create(
    slug="dashboard", defaults={"nome_pt": "Dashboard", "nome_en": "Dashboard", "ordem": 5}
)

print("✓ Categorias criadas")

# Cases data
cases_data = [
    {
        "slug": "loja-virtual-modastyle",
        "categoria": cat_ecommerce,
        "titulo_pt": "Loja Virtual ModaStyle",
        "titulo_en": "ModaStyle Online Store",
        "cliente": "ModaStyle",
        "industria": "Moda Feminina",
        "desafio_pt": "Criar uma loja virtual completa para uma marca de moda feminina, com catálogo de produtos, carrinho de compras, checkout integrado e área do cliente personalizada.",
        "solucao_pt": "Desenvolvemos uma plataforma e-commerce completa com Django e React, incluindo gestão de estoque, integração com gateways de pagamento, sistema de cupons e área do cliente com histórico de pedidos.",
        "resultados_pt": "Aumento de 150% nas vendas online no primeiro trimestre. Taxa de conversão de 3.5%. Tempo médio de carregamento < 2 segundos.",
        "tecnologias": ["Python", "Django", "Django REST Framework", "React"],
        "destaque": True,
        "ativo": True,
        "ordem": 1,
    },
    {
        "slug": "sistema-gestao-clinica-medica",
        "categoria": cat_sistema,
        "titulo_pt": "Sistema de Gestão para Clínica Médica",
        "titulo_en": "Medical Clinic Management System",
        "cliente": "Clínica Saúde+",
        "industria": "Saúde",
        "desafio_pt": "Desenvolver um sistema completo de gestão para clínica médica, incluindo agendamento de consultas, prontuário eletrônico, gestão financeira e relatórios gerenciais.",
        "solucao_pt": "Sistema web completo com módulos integrados de agendamento, prontuário eletrônico (PEP), faturamento, controle financeiro e dashboard gerencial com indicadores em tempo real.",
        "resultados_pt": "Redução de 60% no tempo de agendamento. Eliminação de prontuários em papel. Aumento de 40% na eficiência administrativa.",
        "tecnologias": ["Python", "Django", "PostgreSQL", "JavaScript"],
        "destaque": True,
        "ativo": True,
        "ordem": 2,
    },
    {
        "slug": "marketplace-produtos-artesanais",
        "categoria": cat_ecommerce,
        "titulo_pt": "Marketplace de Produtos Artesanais",
        "titulo_en": "Handmade Products Marketplace",
        "cliente": "ArteBrasil",
        "industria": "Artesanato",
        "desafio_pt": "Criar um marketplace que conecta artesãos brasileiros a compradores, permitindo múltiplos vendedores, gestão de comissões e sistema de avaliações.",
        "solucao_pt": "Plataforma marketplace multi-vendor com sistema de comissões automático, split de pagamentos, avaliações verificadas e painel completo para vendedores.",
        "resultados_pt": "Mais de 500 artesãos cadastrados. Volume de vendas de R$ 200mil/mês. NPS de 4.8/5.",
        "tecnologias": ["Python", "Django", "Django REST Framework", "React"],
        "destaque": False,
        "ativo": True,
        "ordem": 3,
    },
    {
        "slug": "site-institucional-escritorio-advocacia",
        "categoria": cat_institucional,
        "titulo_pt": "Site Institucional Escritório de Advocacia",
        "titulo_en": "Law Firm Institutional Website",
        "cliente": "Advocacia Silva & Associados",
        "industria": "Jurídico",
        "desafio_pt": "Criar um site institucional elegante e profissional para um escritório de advocacia, transmitindo credibilidade e facilitando o contato de potenciais clientes.",
        "solucao_pt": "Site responsivo com design elegante, páginas de áreas de atuação, perfis dos advogados, blog jurídico e formulário de contato integrado com CRM.",
        "resultados_pt": "Aumento de 200% nos contatos via site. Primeira página do Google para termos relevantes. Tempo médio de visita de 4 minutos.",
        "tecnologias": ["Python", "Django", "PostgreSQL", "Bootstrap 5"],
        "destaque": False,
        "ativo": True,
        "ordem": 4,
    },
    {
        "slug": "landing-page-lancamento-imobiliario",
        "categoria": cat_landing,
        "titulo_pt": "Landing Page Lançamento Imobiliário",
        "titulo_en": "Real Estate Launch Landing Page",
        "cliente": "Construtora Premium",
        "industria": "Imobiliário",
        "desafio_pt": "Criar uma landing page de alta conversão para o lançamento de um empreendimento imobiliário de alto padrão, capturando leads qualificados para a equipe de vendas.",
        "solucao_pt": "Landing page otimizada para conversão com tour virtual 360°, plantas interativas, formulário inteligente e integração com ferramentas de marketing.",
        "resultados_pt": "Taxa de conversão de 8.5%. Mais de 2000 leads qualificados. ROI de 15x sobre investimento em mídia.",
        "tecnologias": ["HTML5", "CSS3", "JavaScript", "Bootstrap 5"],
        "destaque": False,
        "ativo": True,
        "ordem": 5,
    },
    {
        "slug": "dashboard-analytics-saas",
        "categoria": cat_dashboard,
        "titulo_pt": "Dashboard de Analytics para SaaS",
        "titulo_en": "SaaS Analytics Dashboard",
        "cliente": "TechMetrics",
        "industria": "Tecnologia / SaaS",
        "desafio_pt": "Desenvolver um dashboard de analytics em tempo real para uma empresa SaaS, permitindo visualização de métricas de uso, receita e comportamento dos usuários.",
        "solucao_pt": "Dashboard interativo com gráficos em tempo real, filtros avançados, exportação de relatórios, alertas automáticos e integração com APIs de dados.",
        "resultados_pt": "Decisões baseadas em dados em tempo real. Redução de 70% no tempo de geração de relatórios. Identificação de churn 30 dias antes.",
        "tecnologias": ["React", "Django REST Framework", "PostgreSQL", "Redis"],
        "destaque": True,
        "ativo": True,
        "ordem": 6,
    },
    {
        "slug": "baby-happy-ecommerce",
        "categoria": cat_ecommerce,
        "titulo_pt": "Baby Happy - Plataforma E-commerce",
        "titulo_en": "Baby Happy - E-commerce Platform",
        "cliente": "Baby Happy",
        "industria": "Varejo / Produtos Infantis",
        "desafio_pt": "Desenvolver uma plataforma e-commerce completa para venda de produtos infantis, com integração de pagamentos Cielo (PIX, Crédito, Débito) e cálculo de frete.",
        "solucao_pt": "Plataforma e-commerce Django com gateway Cielo, integração Melhor Envio, sistema de segurança robusto, painel administrativo completo e deploy com Docker.",
        "resultados_pt": "Plataforma 100% funcional. Processamento seguro de pagamentos. Rate limiting implementado. Zero vulnerabilidades críticas.",
        "tecnologias": ["Python", "Django", "PostgreSQL", "Bootstrap 5", "Docker", "Cielo API"],
        "destaque": True,
        "ativo": True,
        "ordem": 0,
    },
]

# Create cases
for data in cases_data:
    case, created = Case.objects.update_or_create(slug=data["slug"], defaults=data)
    status = "criado" if created else "atualizado"
    print(f"✓ Case {status}: {case.titulo_pt}")

print(f"\n✓ Total: {len(cases_data)} cases adicionados ao portfólio!")
print("Acesse: /portfolio/ para visualizar")
