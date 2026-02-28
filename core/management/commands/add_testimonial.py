"""
Management command to add client testimonials.
"""
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Add client testimonials to the database'

    def handle(self, *args, **options):
        from core.models import Depoimento

        self.stdout.write(self.style.MIGRATE_HEADING('=== Adding Testimonials ===\n'))

        testimonial_data = {
            'nome': 'Baby Happy',
            'empresa': 'E-commerce de Produtos Infantis',
            'depoimento_pt': (
                'A ECOMMDEV entregou nosso e-commerce no prazo e com qualidade acima do esperado. '
                'O site ficou rápido, bonito e nossos clientes elogiam a facilidade de comprar. '
                'Suporte sempre presente. Recomendo!'
            ),
            'avaliacao': 5,
            'ativo': True,
        }

        depoimento, created = Depoimento.objects.get_or_create(
            nome=testimonial_data['nome'],
            empresa=testimonial_data['empresa'],
            defaults={
                'depoimento_pt': testimonial_data['depoimento_pt'],
                'avaliacao': testimonial_data['avaliacao'],
                'ativo': testimonial_data['ativo'],
            },
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f"  ✓ Depoimento adicionado: {depoimento.nome} ({depoimento.empresa}) "
                    f"— avaliação: {depoimento.avaliacao}/5"
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"  ⚠ Depoimento já existia (pulando): {depoimento.nome} ({depoimento.empresa})"
                )
            )

        self.stdout.write(self.style.SUCCESS('\n✓ Depoimentos processados com sucesso!'))
