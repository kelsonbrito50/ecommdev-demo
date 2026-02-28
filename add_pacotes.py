#!/usr/bin/env python
"""Script to add packages to database."""

import os
import sys
import django
from decimal import Decimal

# Setup Django
sys.path.insert(0, "/home/mrdev02/Documents/PROJECTS/ECOMM_DEV")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommdev.settings")
django.setup()

from pacotes.models import Pacote, RecursoPacote

# Delete existing packages and resources
RecursoPacote.objects.all().delete()
Pacote.objects.all().delete()
print("✓ Pacotes existentes removidos")

# Create packages
pacote_basico = Pacote.objects.create(
    tipo="basico",
    nome_pt="Pacote Básico",
    nome_en="Basic Package",
    subtitulo_pt="Ideal para começar",
    subtitulo_en="Ideal to start",
    descricao_pt="Pacote ideal para quem está começando e precisa de uma solução funcional.",
    descricao_en="Ideal package for those starting and need a functional solution.",
    preco=Decimal("10000.00"),
    tempo_desenvolvimento="30 dias úteis",
    suporte_dias=30,
    destaque=False,
    ativo=True,
    ordem=1,
)
print(f"✓ Criado: {pacote_basico.nome_pt}")

# Resources for Básico
recursos_basico = [
    ("Entrega do sistema conforme desenvolvido", True, False),
    ("Instalação em servidor do cliente", True, False),
    ("30 dias de suporte técnico", True, False),
    ("Manual de uso básico", True, False),
]
for titulo, incluido, destaque in recursos_basico:
    RecursoPacote.objects.create(
        pacote=pacote_basico,
        titulo_pt=titulo,
        titulo_en=titulo,
        incluido=incluido,
        destaque=destaque,
        ordem=recursos_basico.index((titulo, incluido, destaque)),
    )

# Pacote Completo
pacote_completo = Pacote.objects.create(
    tipo="completo",
    nome_pt="Pacote Completo",
    nome_en="Complete Package",
    subtitulo_pt="Mais Popular",
    subtitulo_en="Most Popular",
    descricao_pt="Nossa opção mais escolhida. Inclui integrações de pagamento e suporte estendido.",
    descricao_en="Our most chosen option. Includes payment integrations and extended support.",
    preco=Decimal("17000.00"),
    tempo_desenvolvimento="45 dias úteis",
    suporte_dias=90,
    horas_treinamento=4,
    destaque=True,
    ativo=True,
    ordem=2,
)
print(f"✓ Criado: {pacote_completo.nome_pt}")

# Resources for Completo
recursos_completo = [
    ("Tudo do pacote básico", True, False),
    ("Integração com Mercado Pago ou PagSeguro", True, True),
    ("Configuração de domínio e SSL", True, False),
    ("90 dias de suporte", True, False),
    ("Treinamento de 4 horas", True, True),
]
for i, (titulo, incluido, destaque) in enumerate(recursos_completo):
    RecursoPacote.objects.create(
        pacote=pacote_completo,
        titulo_pt=titulo,
        titulo_en=titulo,
        incluido=incluido,
        destaque=destaque,
        ordem=i,
    )

# Pacote Premium
pacote_premium = Pacote.objects.create(
    tipo="premium",
    nome_pt="Pacote Premium",
    nome_en="Premium Package",
    subtitulo_pt="Solução Completa",
    subtitulo_en="Complete Solution",
    descricao_pt="Solução completa com testes automatizados, deploy em nuvem e suporte estendido.",
    descricao_en="Complete solution with automated tests, cloud deploy and extended support.",
    preco=Decimal("25000.00"),
    tempo_desenvolvimento="60 dias úteis",
    suporte_dias=180,
    horas_treinamento=8,
    destaque=False,
    ativo=True,
    ordem=3,
)
print(f"✓ Criado: {pacote_premium.nome_pt}")

# Resources for Premium
recursos_premium = [
    ("Tudo do pacote completo", True, False),
    ("Testes automatizados", True, True),
    ("Docker + deploy em nuvem", True, True),
    ("6 meses de manutenção", True, True),
    ("Customizações adicionais (até 20h)", True, True),
]
for i, (titulo, incluido, destaque) in enumerate(recursos_premium):
    RecursoPacote.objects.create(
        pacote=pacote_premium,
        titulo_pt=titulo,
        titulo_en=titulo,
        incluido=incluido,
        destaque=destaque,
        ordem=i,
    )

print(f"\n✓ Total: 3 pacotes criados com sucesso!")
print("Acesse: /pacotes/ para visualizar")
