"""
Orcamentos App Tests - Orcamento, HistoricoOrcamento
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from orcamentos.models import Orcamento, HistoricoOrcamento

User = get_user_model()


def make_user(email='orc_user@example.com', nome='Orcamento User'):
    return User.objects.create_user(
        email=email,
        password='Senha@123456',
        nome_completo=nome,
        is_active=True,
    )


def make_orcamento(cliente=None, **kwargs):
    defaults = dict(
        nome_completo='Carlos Empresário',
        email='carlos@empresa.com',
        telefone='(85) 99999-9999',
        cidade='Fortaleza',
        estado='CE',
        tipo_projeto='ecommerce',
        descricao_projeto='Quero uma loja online para vender meus produtos.',
    )
    defaults.update(kwargs)
    return Orcamento.objects.create(cliente=cliente, **defaults)


# ─────────────────────────── Orcamento ───────────────────────────────────────

class OrcamentoModelTest(TestCase):
    """Tests for the Orcamento (quote request) model."""

    def setUp(self):
        self.user = make_user()
        self.orcamento = make_orcamento(cliente=self.user)

    def test_str_includes_numero_and_nome(self):
        result = str(self.orcamento)
        self.assertIn('ORC-', result)
        self.assertIn('Carlos Empresário', result)

    def test_numero_auto_generated(self):
        self.assertTrue(self.orcamento.numero.startswith('ORC-'))

    def test_numero_format(self):
        import re
        self.assertRegex(self.orcamento.numero, r'^ORC-\d{4}-\d{4}$')

    def test_default_status_novo(self):
        self.assertEqual(self.orcamento.status, 'novo')

    def test_cliente_relationship(self):
        self.assertEqual(self.orcamento.cliente, self.user)

    def test_related_name_orcamentos(self):
        self.assertIn(self.orcamento, self.user.orcamentos.all())

    def test_nome_completo_field(self):
        self.assertEqual(self.orcamento.nome_completo, 'Carlos Empresário')

    def test_email_field(self):
        self.assertEqual(self.orcamento.email, 'carlos@empresa.com')

    def test_telefone_field(self):
        self.assertEqual(self.orcamento.telefone, '(85) 99999-9999')

    def test_cidade_field(self):
        self.assertEqual(self.orcamento.cidade, 'Fortaleza')

    def test_estado_field(self):
        self.assertEqual(self.orcamento.estado, 'CE')

    def test_tipo_projeto_ecommerce(self):
        self.assertEqual(self.orcamento.tipo_projeto, 'ecommerce')

    def test_all_tipo_projeto_choices(self):
        tipos = ['ecommerce', 'corporativo', 'personalizado', 'manutencao']
        for t in tipos:
            self.orcamento.tipo_projeto = t
            self.orcamento.save()
            self.orcamento.refresh_from_db()
            self.assertEqual(self.orcamento.tipo_projeto, t)

    def test_all_status_choices(self):
        statuses = ['novo', 'em_analise', 'aguardando_info', 'proposta_enviada',
                    'aprovado', 'rejeitado', 'cancelado']
        for s in statuses:
            self.orcamento.status = s
            self.orcamento.save()
            self.orcamento.refresh_from_db()
            self.assertEqual(self.orcamento.status, s)

    def test_optional_fields_default(self):
        self.assertEqual(self.orcamento.empresa, '')
        self.assertEqual(self.orcamento.cnpj, '')
        self.assertEqual(self.orcamento.objetivos, '')
        self.assertEqual(self.orcamento.publico_alvo, '')

    def test_funcionalidades_default_empty_list(self):
        self.assertEqual(self.orcamento.funcionalidades, [])

    def test_integracoes_default_empty_list(self):
        self.assertEqual(self.orcamento.integracoes, [])

    def test_possui_dominio_default_false(self):
        self.assertFalse(self.orcamento.possui_dominio)

    def test_possui_hospedagem_default_false(self):
        self.assertFalse(self.orcamento.possui_hospedagem)

    def test_valor_proposto_optional(self):
        self.assertIsNone(self.orcamento.valor_proposto)

    def test_ip_address_optional(self):
        self.assertIsNone(self.orcamento.ip_address)

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.orcamento.created_at)

    def test_orcamento_without_cliente(self):
        orc = make_orcamento(cliente=None, email='anon@example.com')
        self.assertIsNone(orc.cliente)
        self.assertTrue(orc.numero.startswith('ORC-'))

    def test_sequential_numero_generation(self):
        orc2 = make_orcamento(cliente=self.user, email='orc2@example.com')
        self.assertNotEqual(self.orcamento.numero, orc2.numero)

    def test_ordering_newest_first(self):
        orc2 = make_orcamento(cliente=self.user, email='orc3@example.com')
        orcamentos = list(Orcamento.objects.all())
        self.assertEqual(orcamentos[0].pk, orc2.pk)


# ─────────────────────────── HistoricoOrcamento ───────────────────────────────

class HistoricoOrcamentoModelTest(TestCase):
    """Tests for the HistoricoOrcamento model."""

    def setUp(self):
        self.user = make_user('hist_user@example.com', 'Historico User')
        self.orcamento = make_orcamento(cliente=self.user)
        self.historico = HistoricoOrcamento.objects.create(
            orcamento=self.orcamento,
            usuario=self.user,
            acao='Status alterado',
            status_anterior='novo',
            status_novo='em_analise',
            observacao='Iniciamos a análise do projeto.',
        )

    def test_str_includes_numero_and_acao(self):
        result = str(self.historico)
        self.assertIn(self.orcamento.numero, result)
        self.assertIn('Status alterado', result)

    def test_orcamento_relationship(self):
        self.assertEqual(self.historico.orcamento, self.orcamento)

    def test_related_name_historico(self):
        self.assertIn(self.historico, self.orcamento.historico.all())

    def test_usuario_relationship(self):
        self.assertEqual(self.historico.usuario, self.user)

    def test_acao_field(self):
        self.assertEqual(self.historico.acao, 'Status alterado')

    def test_status_anterior_field(self):
        self.assertEqual(self.historico.status_anterior, 'novo')

    def test_status_novo_field(self):
        self.assertEqual(self.historico.status_novo, 'em_analise')

    def test_observacao_field(self):
        self.assertEqual(self.historico.observacao, 'Iniciamos a análise do projeto.')

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.historico.created_at)

    def test_usuario_optional(self):
        h2 = HistoricoOrcamento.objects.create(
            orcamento=self.orcamento,
            acao='Atualização automática',
        )
        self.assertIsNone(h2.usuario)

    def test_multiple_historico_entries(self):
        HistoricoOrcamento.objects.create(
            orcamento=self.orcamento,
            acao='Proposta enviada',
            status_anterior='em_analise',
            status_novo='proposta_enviada',
        )
        self.assertEqual(self.orcamento.historico.count(), 2)

    def test_ordering_newest_first(self):
        h2 = HistoricoOrcamento.objects.create(
            orcamento=self.orcamento,
            acao='Segunda ação',
        )
        historicos = list(HistoricoOrcamento.objects.filter(orcamento=self.orcamento))
        self.assertEqual(historicos[0].pk, h2.pk)
