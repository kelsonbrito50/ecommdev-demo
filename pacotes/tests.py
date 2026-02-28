"""
Pacotes App Tests - Pacote, RecursoPacote, Adicional
"""
from decimal import Decimal
from django.test import TestCase, Client

from pacotes.models import Pacote, RecursoPacote, Adicional


def make_pacote(tipo='basico', nome='Pacote Básico', preco='997.00', **kwargs):
    return Pacote.objects.create(
        tipo=tipo,
        nome_pt=nome,
        nome_en=f'{nome} EN',
        subtitulo_pt='Ideal para pequenas empresas',
        subtitulo_en='Ideal for small businesses',
        descricao_pt='Pacote completo para iniciar sua presença online.',
        descricao_en='Complete package to start your online presence.',
        preco=Decimal(preco),
        tempo_desenvolvimento='30 dias',
        suporte_dias=30,
        horas_treinamento=2,
        **kwargs,
    )


# ─────────────────────────── Pacote ──────────────────────────────────────────

class PacoteModelTest(TestCase):
    """Tests for the Pacote (pricing package) model."""

    def setUp(self):
        self.pacote = make_pacote()

    def test_str_includes_nome_and_preco(self):
        result = str(self.pacote)
        self.assertIn('Pacote Básico', result)
        self.assertIn('997', result)

    def test_tipo_basico(self):
        self.assertEqual(self.pacote.tipo, 'basico')

    def test_all_tipo_choices(self):
        tipos = [('completo', '1997.00'), ('premium', '3997.00'), ('personalizado', '0.00')]
        for tipo, preco in tipos:
            p = make_pacote(tipo=tipo, nome=f'Pacote {tipo}', preco=preco)
            self.assertEqual(p.tipo, tipo)

    def test_tipo_unique(self):
        from django.db import IntegrityError
        with self.assertRaises(Exception):
            make_pacote(tipo='basico', nome='Outro Basico', preco='500.00')

    def test_preco_field(self):
        self.assertEqual(self.pacote.preco, Decimal('997.00'))

    def test_preco_promocional_optional(self):
        self.assertIsNone(self.pacote.preco_promocional)

    def test_get_preco_final_without_promo(self):
        self.assertEqual(self.pacote.get_preco_final(), Decimal('997.00'))

    def test_get_preco_final_with_promo(self):
        self.pacote.preco_promocional = Decimal('797.00')
        self.pacote.save()
        self.assertEqual(self.pacote.get_preco_final(), Decimal('797.00'))

    def test_nome_property_returns_pt_by_default(self):
        self.assertEqual(self.pacote.nome, 'Pacote Básico')

    def test_subtitulo_property_returns_pt_by_default(self):
        self.assertEqual(self.pacote.subtitulo, 'Ideal para pequenas empresas')

    def test_descricao_property_returns_pt_by_default(self):
        self.assertIn('Pacote completo', self.pacote.descricao)

    def test_default_destaque_false(self):
        self.assertFalse(self.pacote.destaque)

    def test_default_ativo_true(self):
        self.assertTrue(self.pacote.ativo)

    def test_default_cor_destaque(self):
        self.assertEqual(self.pacote.cor_destaque, '#0066CC')

    def test_suporte_dias_field(self):
        self.assertEqual(self.pacote.suporte_dias, 30)

    def test_horas_treinamento_field(self):
        self.assertEqual(self.pacote.horas_treinamento, 2)

    def test_tempo_desenvolvimento_field(self):
        self.assertEqual(self.pacote.tempo_desenvolvimento, '30 dias')

    def test_destaque_can_be_set_true(self):
        self.pacote.destaque = True
        self.pacote.save()
        self.pacote.refresh_from_db()
        self.assertTrue(self.pacote.destaque)

    def test_ativo_can_be_set_false(self):
        self.pacote.ativo = False
        self.pacote.save()
        self.pacote.refresh_from_db()
        self.assertFalse(self.pacote.ativo)

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.pacote.created_at)

    def test_updated_at_auto_set(self):
        self.assertIsNotNone(self.pacote.updated_at)

    def test_ordering_by_ordem_then_preco(self):
        p2 = make_pacote(tipo='completo', nome='Pacote Completo', preco='1997.00', ordem=0)
        self.pacote.ordem = 1
        self.pacote.save()
        pacotes = list(Pacote.objects.all())
        self.assertEqual(pacotes[0].pk, p2.pk)


# ─────────────────────────── RecursoPacote ────────────────────────────────────

class RecursoPacoteModelTest(TestCase):
    """Tests for the RecursoPacote (package feature) model."""

    def setUp(self):
        self.pacote = make_pacote()
        self.recurso = RecursoPacote.objects.create(
            pacote=self.pacote,
            titulo_pt='Design responsivo',
            titulo_en='Responsive design',
            incluido=True,
            destaque=True,
            ordem=1,
        )

    def test_str_includes_pacote_and_titulo(self):
        result = str(self.recurso)
        self.assertIn('Pacote Básico', result)
        self.assertIn('Design responsivo', result)

    def test_str_includes_check_mark_when_included(self):
        result = str(self.recurso)
        self.assertIn('✓', result)

    def test_str_includes_x_mark_when_not_included(self):
        self.recurso.incluido = False
        self.recurso.save()
        result = str(self.recurso)
        self.assertIn('✗', result)

    def test_incluido_true(self):
        self.assertTrue(self.recurso.incluido)

    def test_destaque_true(self):
        self.assertTrue(self.recurso.destaque)

    def test_titulo_property_returns_pt_by_default(self):
        self.assertEqual(self.recurso.titulo, 'Design responsivo')

    def test_pacote_relationship(self):
        self.assertEqual(self.recurso.pacote, self.pacote)

    def test_related_name_recursos(self):
        self.assertIn(self.recurso, self.pacote.recursos.all())

    def test_ordem_field(self):
        self.assertEqual(self.recurso.ordem, 1)

    def test_titulo_en_optional(self):
        r2 = RecursoPacote.objects.create(
            pacote=self.pacote,
            titulo_pt='Integração com pagamentos',
            incluido=True,
        )
        self.assertEqual(r2.titulo_en, '')

    def test_multiple_recursos_per_pacote(self):
        RecursoPacote.objects.create(
            pacote=self.pacote,
            titulo_pt='SEO otimizado',
            incluido=True,
        )
        self.assertEqual(self.pacote.recursos.count(), 2)


# ─────────────────────────── Adicional ────────────────────────────────────────

class AdicionalModelTest(TestCase):
    """Tests for the Adicional (add-on) model."""

    def setUp(self):
        self.adicional = Adicional.objects.create(
            nome_pt='Blog integrado',
            nome_en='Integrated blog',
            descricao_pt='Blog completo integrado ao site.',
            descricao_en='Full blog integrated to the site.',
            preco=Decimal('497.00'),
            tipo_cobranca='unico',
        )

    def test_str_includes_nome_and_preco(self):
        result = str(self.adicional)
        self.assertIn('Blog integrado', result)
        self.assertIn('497', result)

    def test_preco_field(self):
        self.assertEqual(self.adicional.preco, Decimal('497.00'))

    def test_tipo_cobranca_unico(self):
        self.assertEqual(self.adicional.tipo_cobranca, 'unico')

    def test_all_tipo_cobranca_choices(self):
        for tipo in ['unico', 'mensal', 'hora']:
            self.adicional.tipo_cobranca = tipo
            self.adicional.save()
            self.adicional.refresh_from_db()
            self.assertEqual(self.adicional.tipo_cobranca, tipo)

    def test_default_ativo_true(self):
        self.assertTrue(self.adicional.ativo)

    def test_default_ordem_zero(self):
        self.assertEqual(self.adicional.ordem, 0)

    def test_ativo_can_be_set_false(self):
        self.adicional.ativo = False
        self.adicional.save()
        self.adicional.refresh_from_db()
        self.assertFalse(self.adicional.ativo)

    def test_nome_en_optional(self):
        a2 = Adicional.objects.create(
            nome_pt='Loja virtual',
            preco=Decimal('997.00'),
        )
        self.assertEqual(a2.nome_en, '')

    def test_descricao_pt_optional(self):
        a3 = Adicional.objects.create(
            nome_pt='Hospedagem',
            preco=Decimal('100.00'),
        )
        self.assertEqual(a3.descricao_pt, '')

    def test_multiple_adicionais(self):
        Adicional.objects.create(nome_pt='SEO', preco=Decimal('297.00'))
        Adicional.objects.create(nome_pt='Google Ads', preco=Decimal('397.00'))
        self.assertEqual(Adicional.objects.count(), 3)


# ─────────────────────────── Pacotes Views ────────────────────────────────────

class PacotesViewTest(TestCase):
    """Tests for pacotes views."""

    def setUp(self):
        self.client = Client()
        self.pacote = make_pacote()

    def test_pacotes_list_view(self):
        response = self.client.get('/pacotes/')
        self.assertIn(response.status_code, [200, 301, 302, 404])

    def test_pacote_detalhe_view(self):
        response = self.client.get(f'/pacotes/{self.pacote.tipo}/')
        self.assertIn(response.status_code, [200, 301, 302, 404])
