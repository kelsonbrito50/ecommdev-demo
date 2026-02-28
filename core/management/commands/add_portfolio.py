"""
Management command to add portfolio cases.
"""
from django.core.management.base import BaseCommand


CASES = [
    {
        'titulo_pt': 'SecurePass Dashboard',
        'desafio_pt': (
            'Desenvolver um dashboard de segurança corporativa completo para gestão de senhas '
            'e credenciais, com análise de força de senhas e detecção de vazamentos em tempo real.'
        ),
        'solucao_pt': (
            'Dashboard de segurança corporativa para gestão de senhas e credenciais. '
            'Sistema de análise de força de senhas, detecção de vazamentos via HIBP, '
            'autenticação JWT e dashboard interativo com visualização de dados em tempo real.'
        ),
        'tecnologias': ['Python', 'Django REST', 'React', 'TailwindCSS', 'Chart.js'],
        'categoria_nome': 'Sistema Web',
        'url_projeto': 'https://github.com/kelsonbrito50/securepass-dashboard',
    },
    {
        'titulo_pt': 'HireMe AI',
        'desafio_pt': (
            'Criar uma plataforma inteligente de recrutamento com IA capaz de analisar vagas '
            'automaticamente e calcular compatibilidade de candidatos.'
        ),
        'solucao_pt': (
            'Plataforma inteligente de recrutamento com IA. Análise automática de descrições de vagas, '
            'score de compatibilidade de skills (0-100), geração de cover letters com GPT-4, '
            'e dashboard completo de acompanhamento de aplicações.'
        ),
        'tecnologias': ['Next.js', 'TypeScript', 'Prisma', 'PostgreSQL', 'OpenAI GPT-4', 'TailwindCSS'],
        'categoria_nome': 'SaaS',
        'url_projeto': 'https://hireme-ai-rust.vercel.app',
    },
    {
        'titulo_pt': 'Little Lemon Restaurant',
        'desafio_pt': (
            'Desenvolver um sistema de reservas online para restaurante com API REST completa, '
            'gerenciamento de mesas, horários, cardápio dinâmico e painel administrativo.'
        ),
        'solucao_pt': (
            'Sistema de reservas online para restaurante com API REST completa. '
            'Gerenciamento de mesas, horários, cardápio dinâmico e painel administrativo. '
            'Projeto desenvolvido como parte da certificação Meta Back-End Developer Professional Certificate.'
        ),
        'tecnologias': ['Python', 'Django', 'Django REST Framework', 'SQLite'],
        'categoria_nome': 'Sistema Web',
        'url_projeto': '',
    },
]


class Command(BaseCommand):
    help = 'Add portfolio cases to the database'

    def handle(self, *args, **options):
        from portfolio.models import Case, CategoriaPortfolio

        self.stdout.write(self.style.MIGRATE_HEADING('=== Adding Portfolio Cases ===\n'))

        for data in CASES:
            # Find or create the category
            categoria, cat_created = CategoriaPortfolio.objects.get_or_create(
                nome_pt=data['categoria_nome'],
                defaults={'nome_pt': data['categoria_nome']},
            )
            if cat_created:
                self.stdout.write(self.style.WARNING(f"  + Categoria criada: {data['categoria_nome']}"))
            else:
                self.stdout.write(f"  · Categoria existente: {data['categoria_nome']}")

            # Build defaults for the case
            defaults = {
                'desafio_pt': data['desafio_pt'],
                'solucao_pt': data['solucao_pt'],
                'tecnologias': data['tecnologias'],
                'categoria': categoria,
                'ativo': True,
            }
            if data.get('url_projeto'):
                defaults['url_projeto'] = data['url_projeto']

            case, created = Case.objects.get_or_create(
                titulo_pt=data['titulo_pt'],
                defaults=defaults,
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"  ✓ Case adicionado: {data['titulo_pt']}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"  ⚠ Case já existia (pulando): {data['titulo_pt']}")
                )

        self.stdout.write(self.style.SUCCESS('\n✓ Portfolio cases processados com sucesso!'))
