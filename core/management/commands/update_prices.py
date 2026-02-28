"""
Management command to update service and package prices.
"""

from decimal import Decimal

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Update prices for Servicos and Pacotes"

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("=== Updating Servico prices ==="))
        self._update_servicos()

        self.stdout.write(self.style.MIGRATE_HEADING("\n=== Updating Pacote prices ==="))
        self._update_pacotes()

        self.stdout.write(self.style.SUCCESS("\n✓ All prices updated successfully!"))

    def _update_servicos(self):
        from servicos.models import Servico

        # One-time (apartir) services
        apartir_updates = [
            {
                "keyword": "institucional",
                "preco": Decimal("2500.00"),
                "label": "Sites Institucionais",
            },
            {"keyword": "e-commerce", "preco": Decimal("5000.00"), "label": "E-commerce Completo"},
            {"keyword": "ecommerce", "preco": Decimal("5000.00"), "label": "E-commerce Completo"},
            {"keyword": "landing", "preco": Decimal("1200.00"), "label": "Landing Pages"},
            {
                "keyword": "personalizado",
                "preco": Decimal("8000.00"),
                "label": "Sistemas Web Personalizados",
            },
        ]

        for item in apartir_updates:
            qs = Servico.objects.filter(nome_pt__icontains=item["keyword"])
            count = qs.count()
            if count:
                qs.update(preco=item["preco"], tipo_preco="apartir")
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  ✓ [{item['label']}] → R$ {item['preco']:,.2f} (apartir) — {count} registro(s)"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"  ⚠ [{item['label']}] — nenhum registro encontrado (keyword: '{item['keyword']}')"
                    )
                )

        # Monthly plan services
        mensal_updates = [
            {"keyword": "essencial", "preco": Decimal("297.00"), "label": "Plano Essencial"},
            {"keyword": "profissional", "preco": Decimal("597.00"), "label": "Plano Profissional"},
            {"keyword": "premium", "preco": Decimal("1197.00"), "label": "Plano Premium"},
        ]

        for item in mensal_updates:
            qs = Servico.objects.filter(nome_pt__icontains=item["keyword"])
            count = qs.count()
            if count:
                qs.update(preco=item["preco"], tipo_preco="mensal")
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  ✓ [{item['label']}] → R$ {item['preco']:,.2f}/mês — {count} registro(s)"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"  ⚠ [{item['label']}] — nenhum registro encontrado (keyword: '{item['keyword']}')"
                    )
                )

    def _update_pacotes(self):
        from pacotes.models import Pacote

        pacote_updates = [
            {
                "keywords": ["básico", "basico"],
                "preco": Decimal("2000.00"),
                "label": "Pacote Básico",
            },
            {"keywords": ["completo"], "preco": Decimal("4500.00"), "label": "Pacote Completo"},
            {"keywords": ["premium"], "preco": Decimal("8000.00"), "label": "Pacote Premium"},
        ]

        for item in pacote_updates:
            updated_total = 0
            for kw in item["keywords"]:
                qs = Pacote.objects.filter(nome_pt__icontains=kw)
                count = qs.count()
                if count:
                    qs.update(preco=item["preco"])
                    updated_total += count

            if updated_total:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  ✓ [{item['label']}] → R$ {item['preco']:,.2f} — {updated_total} registro(s)"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"  ⚠ [{item['label']}] — nenhum registro encontrado (keywords: {item['keywords']})"
                    )
                )
