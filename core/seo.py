"""
SEO context processor for ECOMMDEV.
Provides default SEO meta tags to all templates and allows per-page override.
"""
from django.conf import settings


# Default SEO configuration
DEFAULT_SEO = {
    'seo_title': 'ECOMMDEV — Desenvolvimento Web Profissional',
    'seo_description': (
        'ECOMMDEV oferece desenvolvimento web profissional para pequenas e médias empresas. '
        'E-commerce, sites corporativos, sistemas personalizados. Atendimento 100% remoto em todo o Brasil.'
    ),
    'seo_keywords': (
        'desenvolvimento web, e-commerce, django, python, sites profissionais, '
        'criação de sites, loja virtual, sistema web, João Pessoa, Brasil'
    ),
    'seo_image': None,  # Falls back to base.html static logo
    'seo_type': 'website',
    'seo_robots': 'index, follow',
}

# Page-specific SEO overrides (path prefix → SEO data)
PAGE_SEO = {
    '/servicos': {
        'seo_title': 'Serviços de Desenvolvimento Web — ECOMMDEV',
        'seo_description': (
            'Conheça nossos serviços: e-commerce, landing pages, sistemas personalizados, '
            'manutenção e muito mais. Soluções web profissionais para seu negócio.'
        ),
    },
    '/pacotes': {
        'seo_title': 'Pacotes de Sites e E-commerce — ECOMMDEV',
        'seo_description': (
            'Pacotes prontos e acessíveis para criar seu site ou loja virtual. '
            'Escolha o plano ideal para seu negócio com entrega rápida e qualidade garantida.'
        ),
    },
    '/portfolio': {
        'seo_title': 'Portfólio de Projetos — ECOMMDEV',
        'seo_description': (
            'Veja nossos cases de sucesso: projetos de e-commerce, sites corporativos e sistemas '
            'desenvolvidos para clientes em todo o Brasil.'
        ),
    },
    '/contato': {
        'seo_title': 'Fale Conosco — ECOMMDEV',
        'seo_description': (
            'Entre em contato com a ECOMMDEV. Atendimento rápido via e-mail. '
            'Solicite um orçamento gratuito para o seu projeto.'
        ),
    },
    '/sobre': {
        'seo_title': 'Sobre a ECOMMDEV — Quem Somos',
        'seo_description': (
            'Conheça a ECOMMDEV: empresa de desenvolvimento web fundada por Kelson Brito. '
            'Especializados em soluções digitais para pequenas e médias empresas.'
        ),
    },
    '/faq': {
        'seo_title': 'Perguntas Frequentes — ECOMMDEV',
        'seo_description': (
            'Tire suas dúvidas sobre os serviços da ECOMMDEV: prazos, preços, tecnologias, '
            'suporte pós-entrega e muito mais.'
        ),
    },
    '/orcamento': {
        'seo_title': 'Solicitar Orçamento Gratuito — ECOMMDEV',
        'seo_description': (
            'Solicite um orçamento gratuito para seu projeto web. '
            'Resposta rápida e proposta personalizada para sua necessidade.'
        ),
    },
}


def seo_context(request):
    """
    Inject SEO meta tag defaults into every template context.

    Templates can override by setting context variables:
      - seo_title
      - seo_description
      - seo_keywords
      - seo_image
      - seo_type
      - seo_robots
    """
    ctx = dict(DEFAULT_SEO)
    ctx['seo_site_url'] = settings.SITE_URL
    ctx['seo_site_name'] = settings.SITE_NAME

    # Apply path-specific overrides
    path = request.path
    for prefix, overrides in PAGE_SEO.items():
        if path.startswith(prefix) or path.startswith('/en' + prefix):
            ctx.update(overrides)
            break

    return ctx
