"""
Management command to seed initial data for ECOMMDEV.
Usage: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from decimal import Decimal

from core.models import ConfiguracaoSite, FAQ
from servicos.models import Servico
from pacotes.models import Pacote, RecursoPacote


class Command(BaseCommand):
    help = 'Seeds the database with initial data for ECOMMDEV'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Seeding initial data...')

        # Site Configuration
        self.seed_site_config()

        # Services
        self.seed_services()

        # Packages
        self.seed_packages()

        # FAQs
        self.seed_faqs()

        self.stdout.write(self.style.SUCCESS('Successfully seeded all data!'))

    def seed_site_config(self):
        if ConfiguracaoSite.objects.exists():
            self.stdout.write('Site configuration already exists, skipping...')
            return

        ConfiguracaoSite.objects.create(
            nome_site_pt='ECOMMDEV',
            nome_site_en='ECOMMDEV',
            tagline_pt='Desenvolvimento Web Profissional',
            tagline_en='Professional Web Development',
            descricao_pt='Desenvolvimento Web Profissional para Pequenas e Médias Empresas em João Pessoa/PB',
            descricao_en='Professional Web Development for Small and Medium Businesses in João Pessoa/PB',
            email_contato='contato@ecommdev.com.br',
            telefone='(83) 99999-9999',
            whatsapp='',
            endereco='João Pessoa, PB - Brasil',
            horario_atendimento='Segunda a Sexta, 9h às 18h',
            linkedin='https://www.linkedin.com/in/kelson-brito-ba922b363',
            instagram='https://www.instagram.com/ecommdev02/',
            github='https://github.com/kelsonbrito50',
            meta_keywords='desenvolvimento web, e-commerce, django, python, joão pessoa',
        )
        self.stdout.write(self.style.SUCCESS('Created site configuration'))

    def seed_services(self):
        if Servico.objects.exists():
            self.stdout.write('Services already exist, skipping...')
            return

        services_data = [
            {
                'nome_pt': 'E-commerce Completo',
                'nome_en': 'Complete E-commerce',
                'slug': 'ecommerce-completo',
                'descricao_curta_pt': 'Loja virtual completa com carrinho, checkout e integração de pagamento',
                'descricao_curta_en': 'Complete online store with cart, checkout and payment integration',
                'descricao_pt': 'Solução completa de e-commerce com gestão de produtos, carrinho de compras, checkout seguro, integração com Mercado Pago e PIX.',
                'descricao_en': 'Complete e-commerce solution with product management, shopping cart, secure checkout, Mercado Pago and PIX integration.',
                'icone': 'bi-cart4',
                'tipo': 'ecommerce',
                'tecnologias': ['Django', 'PostgreSQL', 'Bootstrap', 'Mercado Pago'],
                'ordem': 1,
                'destaque': True,
            },
            {
                'nome_pt': 'Site Corporativo',
                'nome_en': 'Corporate Website',
                'slug': 'site-corporativo',
                'descricao_curta_pt': 'Site institucional profissional para sua empresa',
                'descricao_curta_en': 'Professional institutional website for your company',
                'descricao_pt': 'Site institucional moderno e responsivo, com páginas de serviços, sobre, contato e blog integrado.',
                'descricao_en': 'Modern and responsive institutional website with service pages, about, contact and integrated blog.',
                'icone': 'bi-building',
                'tipo': 'corporativo',
                'tecnologias': ['Django', 'PostgreSQL', 'Bootstrap'],
                'ordem': 2,
                'destaque': True,
            },
            {
                'nome_pt': 'Sistema Personalizado',
                'nome_en': 'Custom System',
                'slug': 'sistema-personalizado',
                'descricao_curta_pt': 'Desenvolvimento sob medida para suas necessidades',
                'descricao_curta_en': 'Custom development for your needs',
                'descricao_pt': 'Desenvolvimento de sistemas web personalizados, incluindo CRMs, ERPs, portais e dashboards.',
                'descricao_en': 'Custom web systems development including CRMs, ERPs, portals and dashboards.',
                'icone': 'bi-gear',
                'tipo': 'personalizado',
                'tecnologias': ['Django', 'PostgreSQL', 'REST API', 'React'],
                'ordem': 3,
                'destaque': False,
            },
            {
                'nome_pt': 'Manutenção e Suporte',
                'nome_en': 'Maintenance and Support',
                'slug': 'manutencao-suporte',
                'descricao_curta_pt': 'Suporte técnico contínuo para seu projeto',
                'descricao_curta_en': 'Continuous technical support for your project',
                'descricao_pt': 'Serviço de manutenção mensal com atualizações de segurança, backup e suporte técnico.',
                'descricao_en': 'Monthly maintenance service with security updates, backup and technical support.',
                'icone': 'bi-headset',
                'tipo': 'manutencao',
                'tecnologias': [],
                'ordem': 4,
                'destaque': False,
            },
        ]

        for data in services_data:
            Servico.objects.create(**data)

        self.stdout.write(self.style.SUCCESS(f'Created {len(services_data)} services'))

    def seed_packages(self):
        if Pacote.objects.exists():
            self.stdout.write('Packages already exist, skipping...')
            return

        packages_data = [
            {
                'nome_pt': 'Pacote Básico',
                'nome_en': 'Basic Package',
                'subtitulo_pt': 'Ideal para começar',
                'subtitulo_en': 'Ideal to start',
                'descricao_pt': 'Sistema completo entregue e instalado no seu servidor',
                'descricao_en': 'Complete system delivered and installed on your server',
                'tipo': 'basico',
                'preco': Decimal('10000.00'),
                'tempo_desenvolvimento': '30 dias úteis',
                'suporte_dias': 30,
                'horas_treinamento': 0,
                'ordem': 1,
                'destaque': False,
                'recursos': [
                    ('Entrega do sistema conforme desenvolvido', 'System delivery as developed', True),
                    ('Instalação em servidor do cliente', 'Installation on client server', True),
                    ('30 dias de suporte técnico', '30 days of technical support', True),
                    ('Manual de uso básico', 'Basic user manual', True),
                ]
            },
            {
                'nome_pt': 'Pacote Completo',
                'nome_en': 'Complete Package',
                'subtitulo_pt': 'Mais Popular',
                'subtitulo_en': 'Most Popular',
                'descricao_pt': 'Solução completa com integração de pagamentos e configuração profissional',
                'descricao_en': 'Complete solution with payment integration and professional configuration',
                'tipo': 'completo',
                'preco': Decimal('17000.00'),
                'tempo_desenvolvimento': '45 dias úteis',
                'suporte_dias': 90,
                'horas_treinamento': 4,
                'ordem': 2,
                'destaque': True,
                'recursos': [
                    ('Tudo do pacote básico', 'Everything from basic package', True),
                    ('Integração com Mercado Pago ou PagSeguro', 'Mercado Pago or PagSeguro integration', True),
                    ('Configuração de domínio e SSL', 'Domain and SSL configuration', True),
                    ('90 dias de suporte', '90 days of support', True),
                    ('Treinamento de 4 horas', '4 hours of training', True),
                ]
            },
            {
                'nome_pt': 'Pacote Premium',
                'nome_en': 'Premium Package',
                'subtitulo_pt': 'Solução Completa',
                'subtitulo_en': 'Complete Solution',
                'descricao_pt': 'A solução mais completa com deploy em nuvem e manutenção estendida',
                'descricao_en': 'The most complete solution with cloud deployment and extended maintenance',
                'tipo': 'premium',
                'preco': Decimal('25000.00'),
                'tempo_desenvolvimento': '60 dias úteis',
                'suporte_dias': 180,
                'horas_treinamento': 4,
                'ordem': 3,
                'destaque': False,
                'recursos': [
                    ('Tudo do pacote completo', 'Everything from complete package', True),
                    ('Testes automatizados', 'Automated tests', True),
                    ('Docker + deploy em nuvem', 'Docker + cloud deployment', True),
                    ('6 meses de manutenção', '6 months of maintenance', True),
                    ('Customizações adicionais (até 20h)', 'Additional customizations (up to 20h)', True),
                ]
            },
        ]

        for data in packages_data:
            recursos = data.pop('recursos')
            pacote = Pacote.objects.create(**data)

            for idx, (titulo_pt, titulo_en, incluido) in enumerate(recursos):
                RecursoPacote.objects.create(
                    pacote=pacote,
                    titulo_pt=titulo_pt,
                    titulo_en=titulo_en,
                    incluido=incluido,
                    ordem=idx + 1
                )

        self.stdout.write(self.style.SUCCESS(f'Created {len(packages_data)} packages with resources'))

    def seed_faqs(self):
        if FAQ.objects.exists():
            self.stdout.write('FAQs already exist, skipping...')
            return

        faqs_data = [
            {
                'categoria': 'geral',
                'pergunta_pt': 'Quanto tempo leva para criar um site?',
                'pergunta_en': 'How long does it take to create a website?',
                'resposta_pt': 'O prazo varia de acordo com a complexidade do projeto. Um site institucional básico pode ser entregue em 10 dias úteis, enquanto um e-commerce completo pode levar de 20 a 30 dias úteis.',
                'resposta_en': 'The timeline varies according to the project complexity. A basic institutional website can be delivered in 10 business days, while a complete e-commerce can take 20 to 30 business days.',
                'ordem': 1,
            },
            {
                'categoria': 'pagamento',
                'pergunta_pt': 'Quais formas de pagamento são aceitas?',
                'pergunta_en': 'What payment methods are accepted?',
                'resposta_pt': 'Aceitamos PIX, boleto bancário e cartão de crédito (em até 12x). O pagamento é dividido em 50% na aprovação do orçamento e 50% na entrega do projeto.',
                'resposta_en': 'We accept PIX, bank slip and credit card (up to 12 installments). Payment is split into 50% upon quote approval and 50% upon project delivery.',
                'ordem': 2,
            },
            {
                'categoria': 'geral',
                'pergunta_pt': 'O site será responsivo (funciona no celular)?',
                'pergunta_en': 'Will the website be responsive (work on mobile)?',
                'resposta_pt': 'Sim! Todos os nossos projetos são desenvolvidos com design responsivo.',
                'resposta_en': 'Yes! All our projects are developed with responsive design.',
                'ordem': 3,
            },
            {
                'categoria': 'servicos',
                'pergunta_pt': 'Vocês oferecem hospedagem?',
                'pergunta_en': 'Do you offer hosting?',
                'resposta_pt': 'Sim, oferecemos planos de hospedagem com suporte técnico, backup diário e certificado SSL.',
                'resposta_en': 'Yes, we offer hosting plans with technical support, daily backup and SSL certificate.',
                'ordem': 4,
            },
            {
                'categoria': 'suporte',
                'pergunta_pt': 'Como funciona o suporte pós-entrega?',
                'pergunta_en': 'How does post-delivery support work?',
                'resposta_pt': 'Oferecemos 30 dias de suporte gratuito após a entrega para ajustes e dúvidas.',
                'resposta_en': 'We offer 30 days of free support after delivery for adjustments and questions.',
                'ordem': 5,
            },
        ]

        for data in faqs_data:
            FAQ.objects.create(**data)

        self.stdout.write(self.style.SUCCESS(f'Created {len(faqs_data)} FAQs'))
