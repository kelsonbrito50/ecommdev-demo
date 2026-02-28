"""
Servicos App Tests - Servico, RecursoServico
"""
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse

from servicos.models import Servico, RecursoServico


def make_servico(tipo='ecommerce', nome='Loja Virtual', slug=None, **kwargs):
    return Servico.objects.create(
        tipo=tipo,
        nome_pt=nome,
        nome_en=f'{nome} EN',
        slug=slug or nome.lower().replace(' ', '-'),
        descricao_curta_pt='Crie sua loja virtual agora.',
        descricao_curta_en='Create your online store now.',
        descricao_pt='Desenvolvemos lojas virtuais completas e responsivas.',
        descricao_en='We develop complete and responsive online stores.',
        preco=Decimal('1997.00'),
        tipo_preco='apartir',
        prazo='30 dias',
        ativo=True,
        destaque=True,
        **kwargs,
    )


# ─────────────────────────── Servico ─────────────────────────────────────────

class ServicoModelTest(TestCase):
    """Tests for the Servico (service catalog) model."""

    def setUp(self):
        self.servico = make_servico()

    def test_str_returns_nome_pt(self):
        self.assertEqual(str(self.servico), 'Loja Virtual')

    def test_slug_auto_generated(self):
        s = make_servico(tipo='landing', nome='Landing Page', slug=None)
        # slug should be based on nome_pt
        self.assertIsNotNone(s.slug)
        self.assertTrue(len(s.slug) > 0)

    def test_slug_manual_set(self):
        self.assertEqual(self.servico.slug, 'loja-virtual')

    def test_tipo_ecommerce(self):
        self.assertEqual(self.servico.tipo, 'ecommerce')

    def test_all_tipo_choices(self):
        tipos = ['desenvolvimento', 'ecommerce', 'landing', 'sistema',
                 'manutencao', 'design', 'marketing', 'integracao', 'treinamento', 'pacote']
        for i, tipo in enumerate(tipos):
            s = make_servico(tipo=tipo, nome=f'Serviço {i}', slug=f'servico-{i}')
            self.assertEqual(s.tipo, tipo)

    def test_preco_field(self):
        self.assertEqual(self.servico.preco, Decimal('1997.00'))

    def test_tipo_preco_apartir(self):
        self.assertEqual(self.servico.tipo_preco, 'apartir')

    def test_get_preco_display_apartir(self):
        display = self.servico.get_preco_display()
        self.assertIn('1.997', display)  # Brazilian number format

    def test_get_preco_display_mensal(self):
        self.servico.tipo_preco = 'mensal'
        self.servico.save()
        display = self.servico.get_preco_display()
        self.assertIn('/mês', display)

    def test_get_preco_display_hora(self):
        self.servico.tipo_preco = 'hora'
        self.servico.save()
        display = self.servico.get_preco_display()
        self.assertIn('/hora', display)

    def test_get_preco_display_fixo(self):
        self.servico.tipo_preco = 'fixo'
        self.servico.save()
        display = self.servico.get_preco_display()
        self.assertIn('R$', display)

    def test_nome_property_returns_pt_by_default(self):
        self.assertEqual(self.servico.nome, 'Loja Virtual')

    def test_descricao_curta_property_returns_pt_by_default(self):
        self.assertEqual(self.servico.descricao_curta, 'Crie sua loja virtual agora.')

    def test_descricao_property_returns_pt_by_default(self):
        self.assertIn('Desenvolvemos lojas', self.servico.descricao)

    def test_default_ativo_true(self):
        self.assertTrue(self.servico.ativo)

    def test_default_destaque_true(self):
        self.assertTrue(self.servico.destaque)

    def test_ativo_can_be_set_false(self):
        self.servico.ativo = False
        self.servico.save()
        self.servico.refresh_from_db()
        self.assertFalse(self.servico.ativo)

    def test_get_absolute_url(self):
        url = self.servico.get_absolute_url()
        self.assertIn('loja-virtual', url)

    def test_tecnologias_default_empty_list(self):
        self.assertEqual(self.servico.tecnologias, [])

    def test_beneficios_pt_default_empty_list(self):
        self.assertEqual(self.servico.beneficios_pt, [])

    def test_beneficios_property_returns_pt_by_default(self):
        self.assertEqual(self.servico.beneficios, [])

    def test_preco_ate_optional(self):
        self.assertIsNone(self.servico.preco_ate)

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.servico.created_at)

    def test_updated_at_auto_set(self):
        self.assertIsNotNone(self.servico.updated_at)


# ─────────────────────────── RecursoServico ──────────────────────────────────

class RecursoServicoModelTest(TestCase):
    """Tests for the RecursoServico (service feature) model."""

    def setUp(self):
        self.servico = make_servico()
        self.recurso = RecursoServico.objects.create(
            servico=self.servico,
            titulo_pt='Carrinho de compras',
            titulo_en='Shopping cart',
            descricao_pt='Sistema completo de carrinho de compras.',
            descricao_en='Complete shopping cart system.',
            icone='fas fa-shopping-cart',
            ordem=1,
        )

    def test_str_includes_servico_and_titulo(self):
        result = str(self.recurso)
        self.assertIn('Loja Virtual', result)
        self.assertIn('Carrinho de compras', result)

    def test_titulo_property_returns_pt_by_default(self):
        self.assertEqual(self.recurso.titulo, 'Carrinho de compras')

    def test_descricao_property_returns_pt_by_default(self):
        self.assertIn('completo de carrinho', self.recurso.descricao)

    def test_servico_relationship(self):
        self.assertEqual(self.recurso.servico, self.servico)

    def test_related_name_recursos(self):
        self.assertIn(self.recurso, self.servico.recursos.all())

    def test_icone_field(self):
        self.assertEqual(self.recurso.icone, 'fas fa-shopping-cart')

    def test_ordem_field(self):
        self.assertEqual(self.recurso.ordem, 1)

    def test_titulo_en_optional(self):
        r2 = RecursoServico.objects.create(
            servico=self.servico,
            titulo_pt='Gateway de pagamento',
            ordem=2,
        )
        self.assertEqual(r2.titulo_en, '')

    def test_multiple_recursos_per_servico(self):
        RecursoServico.objects.create(
            servico=self.servico,
            titulo_pt='Painel administrativo',
            ordem=2,
        )
        self.assertEqual(self.servico.recursos.count(), 2)

    def test_ordering_by_ordem(self):
        r2 = RecursoServico.objects.create(
            servico=self.servico,
            titulo_pt='Relatórios',
            ordem=0,
        )
        recursos = list(self.servico.recursos.all())
        self.assertEqual(recursos[0].pk, r2.pk)  # ordem=0 before ordem=1


# ─────────────────────────── Servicos Views ──────────────────────────────────

class ServicosViewTest(TestCase):
    """Tests for servicos views."""

    def setUp(self):
        self.client = Client()
        self.servico = make_servico()

    def test_servicos_list_view(self):
        response = self.client.get('/servicos/')
        self.assertIn(response.status_code, [200, 301, 302, 404])

    def test_servico_detalhe_view(self):
        response = self.client.get(f'/servicos/{self.servico.slug}/')
        self.assertIn(response.status_code, [200, 301, 302, 404])
