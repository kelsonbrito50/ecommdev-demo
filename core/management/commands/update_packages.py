"""
Management command to update package data for ECOMMDEV.
Usage: python manage.py update_packages
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from decimal import Decimal

from pacotes.models import Pacote, RecursoPacote


class Command(BaseCommand):
    help = 'Updates packages with new pricing and features'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Updating packages...')

        packages_data = [
            {
                'tipo': 'basico',
                'nome_pt': 'Pacote Básico',
                'nome_en': 'Basic Package',
                'subtitulo_pt': 'Ideal para começar',
                'subtitulo_en': 'Ideal to start',
                'descricao_pt': 'Sistema completo entregue e instalado no seu servidor',
                'descricao_en': 'Complete system delivered and installed on your server',
                'preco': Decimal('10000.00'),
                'preco_promocional': None,
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
                'tipo': 'completo',
                'nome_pt': 'Pacote Completo',
                'nome_en': 'Complete Package',
                'subtitulo_pt': 'Mais Popular',
                'subtitulo_en': 'Most Popular',
                'descricao_pt': 'Solução completa com integração de pagamentos e configuração profissional',
                'descricao_en': 'Complete solution with payment integration and professional configuration',
                'preco': Decimal('17000.00'),
                'preco_promocional': None,
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
                'tipo': 'premium',
                'nome_pt': 'Pacote Premium',
                'nome_en': 'Premium Package',
                'subtitulo_pt': 'Solução Completa',
                'subtitulo_en': 'Complete Solution',
                'descricao_pt': 'A solução mais completa com deploy em nuvem e manutenção estendida',
                'descricao_en': 'The most complete solution with cloud deployment and extended maintenance',
                'preco': Decimal('25000.00'),
                'preco_promocional': None,
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
            tipo = data.pop('tipo')
            recursos = data.pop('recursos')

            # Update or create package
            pacote, created = Pacote.objects.update_or_create(
                tipo=tipo,
                defaults=data
            )

            action = 'Created' if created else 'Updated'
            self.stdout.write(f'{action}: {pacote.nome_pt} - R$ {pacote.preco:,.2f}')

            # Delete existing resources and create new ones
            pacote.recursos.all().delete()

            for idx, (titulo_pt, titulo_en, incluido) in enumerate(recursos):
                RecursoPacote.objects.create(
                    pacote=pacote,
                    titulo_pt=titulo_pt,
                    titulo_en=titulo_en,
                    incluido=incluido,
                    ordem=idx + 1
                )

            self.stdout.write(f'  - {len(recursos)} recursos atualizados')

        self.stdout.write(self.style.SUCCESS('Packages updated successfully!'))
