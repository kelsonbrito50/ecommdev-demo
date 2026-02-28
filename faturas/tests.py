"""
Faturas App Tests - Fatura, ItemFatura, Pagamento
"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from faturas.models import Fatura, ItemFatura, Pagamento

User = get_user_model()


def make_user(email="fat_user@example.com", nome="Fatura User"):
    return User.objects.create_user(
        email=email,
        password="Senha@123456",
        nome_completo=nome,
        is_active=True,
    )


# ─────────────────────────── Fatura ─────────────────────────────────────────


class FaturaModelTest(TestCase):
    """Tests for the Fatura (invoice) model."""

    def setUp(self):
        self.user = make_user()
        import datetime

        self.fatura = Fatura.objects.create(
            cliente=self.user,
            data_vencimento=datetime.date.today(),
            subtotal=Decimal("1000.00"),
            desconto=Decimal("100.00"),
            impostos=Decimal("50.00"),
        )

    def test_str_includes_numero_and_valor(self):
        result = str(self.fatura)
        self.assertIn("INV-", result)

    def test_numero_auto_generated(self):
        self.assertTrue(self.fatura.numero.startswith("INV-"))

    def test_numero_format(self):
        self.assertRegex(self.fatura.numero, r"^INV-\d{4}-\d{4}$")

    def test_valor_total_calculated(self):
        # valor_total = subtotal - desconto + impostos = 1000 - 100 + 50 = 950
        self.assertEqual(self.fatura.valor_total, Decimal("950.00"))

    def test_default_status_pendente(self):
        self.assertEqual(self.fatura.status, "pendente")

    def test_status_color_pendente(self):
        self.assertEqual(self.fatura.status_color, "warning")

    def test_status_color_paga(self):
        self.fatura.status = "paga"
        self.assertEqual(self.fatura.status_color, "success")

    def test_status_color_vencida(self):
        self.fatura.status = "vencida"
        self.assertEqual(self.fatura.status_color, "danger")

    def test_status_color_cancelada(self):
        self.fatura.status = "cancelada"
        self.assertEqual(self.fatura.status_color, "secondary")

    def test_cliente_relationship(self):
        self.assertEqual(self.fatura.cliente, self.user)

    def test_related_name_faturas(self):
        self.assertIn(self.fatura, self.user.faturas.all())

    def test_projeto_is_optional(self):
        self.assertIsNone(self.fatura.projeto)

    def test_data_pagamento_is_optional(self):
        self.assertIsNone(self.fatura.data_pagamento)

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.fatura.created_at)

    def test_updated_at_auto_set(self):
        self.assertIsNotNone(self.fatura.updated_at)

    def test_sequential_numero_generation(self):
        import datetime

        fatura2 = Fatura.objects.create(
            cliente=self.user,
            data_vencimento=datetime.date.today(),
        )
        # Both should have unique numbers
        self.assertNotEqual(self.fatura.numero, fatura2.numero)

    def test_all_status_choices(self):
        valid_statuses = ["rascunho", "pendente", "paga", "vencida", "cancelada", "reembolsada"]
        for s in valid_statuses:
            self.fatura.status = s
            self.fatura.save()
            self.fatura.refresh_from_db()
            self.assertEqual(self.fatura.status, s)

    def test_observacoes_default_blank(self):
        self.assertEqual(self.fatura.observacoes, "")

    def test_observacoes_internas_default_blank(self):
        self.assertEqual(self.fatura.observacoes_internas, "")


# ─────────────────────────── ItemFatura ─────────────────────────────────────


class ItemFaturaModelTest(TestCase):
    """Tests for the ItemFatura (invoice line item) model."""

    def setUp(self):
        import datetime

        self.user = make_user("item_user@example.com", "Item User")
        self.fatura = Fatura.objects.create(
            cliente=self.user,
            data_vencimento=datetime.date.today(),
        )
        self.item = ItemFatura.objects.create(
            fatura=self.fatura,
            descricao="Desenvolvimento de Landing Page",
            quantidade=2,
            valor_unitario=Decimal("500.00"),
        )

    def test_str_includes_descricao(self):
        result = str(self.item)
        self.assertIn("Desenvolvimento de Landing Page", result)

    def test_subtotal_auto_calculated(self):
        self.assertEqual(self.item.subtotal, Decimal("1000.00"))

    def test_subtotal_recalculated_on_save(self):
        self.item.quantidade = 3
        self.item.save()
        self.item.refresh_from_db()
        self.assertEqual(self.item.subtotal, Decimal("1500.00"))

    def test_fatura_relationship(self):
        self.assertEqual(self.item.fatura, self.fatura)

    def test_related_name_itens(self):
        self.assertIn(self.item, self.fatura.itens.all())

    def test_quantidade_field(self):
        self.assertEqual(self.item.quantidade, 2)

    def test_valor_unitario_field(self):
        self.assertEqual(self.item.valor_unitario, Decimal("500.00"))

    def test_multiple_items_on_same_invoice(self):
        ItemFatura.objects.create(
            fatura=self.fatura,
            descricao="Hospedagem",
            quantidade=1,
            valor_unitario=Decimal("100.00"),
        )
        self.assertEqual(self.fatura.itens.count(), 2)


# ─────────────────────────── Pagamento ──────────────────────────────────────


class PagamentoModelTest(TestCase):
    """Tests for the Pagamento (payment record) model."""

    def setUp(self):
        import datetime

        self.user = make_user("pag_user@example.com", "Pagamento User")
        self.fatura = Fatura.objects.create(
            cliente=self.user,
            data_vencimento=datetime.date.today(),
            subtotal=Decimal("500.00"),
        )
        self.pagamento = Pagamento.objects.create(
            fatura=self.fatura,
            metodo="pix",
            valor=Decimal("500.00"),
            status="aprovado",
            transacao_id="TXN-12345",
        )

    def test_str_includes_fatura_numero_and_metodo(self):
        result = str(self.pagamento)
        self.assertIn(self.fatura.numero, result)
        self.assertIn("pix", result)

    def test_default_status_pendente(self):
        import datetime

        fatura2 = Fatura.objects.create(
            cliente=self.user,
            data_vencimento=datetime.date.today(),
        )
        pag2 = Pagamento.objects.create(
            fatura=fatura2,
            metodo="boleto",
            valor=Decimal("200.00"),
        )
        self.assertEqual(pag2.status, "pendente")

    def test_status_is_aprovado(self):
        self.assertEqual(self.pagamento.status, "aprovado")

    def test_metodo_pix(self):
        self.assertEqual(self.pagamento.metodo, "pix")

    def test_valor_field(self):
        self.assertEqual(self.pagamento.valor, Decimal("500.00"))

    def test_transacao_id_stored(self):
        self.assertEqual(self.pagamento.transacao_id, "TXN-12345")

    def test_default_gateway_mercadopago(self):
        self.assertEqual(self.pagamento.gateway, "mercadopago")

    def test_dados_gateway_default_empty_dict(self):
        self.assertEqual(self.pagamento.dados_gateway, {})

    def test_related_name_pagamentos(self):
        self.assertIn(self.pagamento, self.fatura.pagamentos.all())

    def test_all_metodo_choices(self):
        import datetime

        metodos = ["pix", "boleto", "cartao_credito", "cartao_debito", "transferencia"]
        for _i, metodo in enumerate(metodos):
            f = Fatura.objects.create(
                cliente=self.user,
                data_vencimento=datetime.date.today(),
            )
            p = Pagamento.objects.create(fatura=f, metodo=metodo, valor=Decimal("100.00"))
            self.assertEqual(p.metodo, metodo)

    def test_data_pagamento_optional(self):
        self.assertIsNone(self.pagamento.data_pagamento)

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.pagamento.created_at)
