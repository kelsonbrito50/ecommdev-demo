"""
Management command: load_demo_data

Clears existing services/packages data and loads the AI services fixtures.

Usage:
    python manage.py load_demo_data
"""

import os

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Clear old data and load AI services + packages fixtures"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("⚙️  Starting load_demo_data..."))

        # --- 1. Clear existing data ---
        self.stdout.write("🗑️  Clearing old data...")
        self._clear_data()

        # --- 2. Load AI services fixture ---
        servicos_fixture = self._find_fixture("servicos_data.json")
        if servicos_fixture:
            self.stdout.write(f"📦 Loading services fixture: {servicos_fixture}")
            call_command("loaddata", servicos_fixture, verbosity=0)
        else:
            self.stdout.write(self.style.ERROR("❌ servicos_data.json not found!"))

        # --- 3. Load packages fixture ---
        pacotes_fixture = self._find_fixture("pacotes_data.json")
        if pacotes_fixture:
            self.stdout.write(f"📦 Loading packages fixture: {pacotes_fixture}")
            call_command("loaddata", pacotes_fixture, verbosity=0)
        else:
            self.stdout.write(self.style.ERROR("❌ pacotes_data.json not found!"))

        # --- 4. Print summary ---
        self._print_summary()

    def _find_fixture(self, filename):
        """Find fixture file in fixtures/ dir or project root."""
        base = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        )
        candidates = [
            os.path.join(base, "fixtures", filename),
            os.path.join(base, filename),
        ]
        for path in candidates:
            if os.path.exists(path):
                return path
        return None

    def _clear_data(self):
        """Delete all existing services and packages records."""
        from pacotes.models import Adicional, Pacote, RecursoPacote
        from servicos.models import RecursoServico, Servico

        counts = {
            "RecursoServico": RecursoServico.objects.count(),
            "Servico": Servico.objects.count(),
            "RecursoPacote": RecursoPacote.objects.count(),
            "Adicional": Adicional.objects.count(),
            "Pacote": Pacote.objects.count(),
        }
        RecursoServico.objects.all().delete()
        Servico.objects.all().delete()
        RecursoPacote.objects.all().delete()
        Adicional.objects.all().delete()
        Pacote.objects.all().delete()
        for model, count in counts.items():
            if count:
                self.stdout.write(f"   Deleted {count} {model} records")

    def _print_summary(self):
        """Print a summary of loaded data."""
        from pacotes.models import Adicional, Pacote, RecursoPacote
        from servicos.models import Servico

        servicos_count = Servico.objects.filter(ativo=True).count()
        pacotes_count = Pacote.objects.filter(ativo=True).count()
        recursos_count = RecursoPacote.objects.count()
        adicionais_count = Adicional.objects.count()

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("✅ Data loaded successfully!"))
        self.stdout.write(self.style.SUCCESS("=" * 50))
        self.stdout.write(self.style.SUCCESS(f"  🤖 AI Services (active) : {servicos_count}"))
        self.stdout.write(self.style.SUCCESS(f"  📦 Packages (active)    : {pacotes_count}"))
        self.stdout.write(self.style.SUCCESS(f"  📋 Package Resources    : {recursos_count}"))
        self.stdout.write(self.style.SUCCESS(f"  ➕ Add-ons              : {adicionais_count}"))
        self.stdout.write(self.style.SUCCESS("=" * 50))
        self.stdout.write("")

        if pacotes_count:
            from pacotes.models import Pacote

            self.stdout.write("  Packages loaded:")
            for p in Pacote.objects.filter(ativo=True).order_by("ordem"):
                self.stdout.write(f"    • {p.nome_pt} — R$ {p.preco:,.2f}")
            self.stdout.write("")

        if servicos_count:
            self.stdout.write("  Services loaded:")
            for s in Servico.objects.filter(ativo=True).order_by("ordem"):
                self.stdout.write(f"    • {s.nome_pt}")
            self.stdout.write("")
