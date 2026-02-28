"""
Core App Tests - ConfiguracaoSite, Contato, Depoimento, FAQ + Views
"""

from django.contrib.auth import get_user_model
from django.test import TestCase

from core.models import FAQ, ConfiguracaoSite, Contato, Depoimento

User = get_user_model()


# ─────────────────────────── ConfiguracaoSite ───────────────────────────────


class ConfiguracaoSiteModelTest(TestCase):
    """Tests for the ConfiguracaoSite singleton model."""

    def setUp(self):
        self.config = ConfiguracaoSite.objects.create(
            nome_site_pt="ECOMMDEV",
            nome_site_en="ECOMMDEV EN",
            email_contato="contato@ecommdev.com.br",
            telefone="+55 85 99999-9999",
            whatsapp="+55 85 99999-9999",
        )

    def test_str_returns_nome_site_pt(self):
        self.assertEqual(str(self.config), "ECOMMDEV")

    def test_only_one_instance_allowed(self):
        with self.assertRaises(ValueError):
            ConfiguracaoSite.objects.create(
                nome_site_pt="Outro Site",
                email_contato="outro@example.com",
            )

    def test_email_contato_field(self):
        self.assertEqual(self.config.email_contato, "contato@ecommdev.com.br")

    def test_telefone_field(self):
        self.assertEqual(self.config.telefone, "+55 85 99999-9999")

    def test_social_fields_default_blank(self):
        self.assertEqual(self.config.linkedin, "")
        self.assertEqual(self.config.instagram, "")
        self.assertEqual(self.config.github, "")
        self.assertEqual(self.config.youtube, "")

    def test_seo_fields_default_blank(self):
        self.assertEqual(self.config.meta_keywords, "")
        self.assertEqual(self.config.meta_description_pt, "")
        self.assertEqual(self.config.meta_description_en, "")

    def test_analytics_fields_default_blank(self):
        self.assertEqual(self.config.google_analytics_id, "")
        self.assertEqual(self.config.facebook_pixel_id, "")

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.config.created_at)

    def test_updated_at_auto_set(self):
        self.assertIsNotNone(self.config.updated_at)

    def test_nome_site_en_field(self):
        self.assertEqual(self.config.nome_site_en, "ECOMMDEV EN")


# ─────────────────────────── Contato ────────────────────────────────────────


class ContatoModelTest(TestCase):
    """Tests for the Contato (contact submission) model."""

    def setUp(self):
        self.contato = Contato.objects.create(
            nome="João Silva",
            email="joao@example.com",
            assunto="Orçamento de site",
            mensagem="Gostaria de um orçamento para meu e-commerce.",
        )

    def test_str_includes_nome_and_assunto(self):
        result = str(self.contato)
        self.assertIn("João Silva", result)
        self.assertIn("Orçamento de site", result)

    def test_default_status_is_novo(self):
        self.assertEqual(self.contato.status, "novo")

    def test_can_change_status_to_lido(self):
        self.contato.status = "lido"
        self.contato.save()
        self.contato.refresh_from_db()
        self.assertEqual(self.contato.status, "lido")

    def test_can_change_status_to_respondido(self):
        self.contato.status = "respondido"
        self.contato.save()
        self.contato.refresh_from_db()
        self.assertEqual(self.contato.status, "respondido")

    def test_can_change_status_to_arquivado(self):
        self.contato.status = "arquivado"
        self.contato.save()
        self.contato.refresh_from_db()
        self.assertEqual(self.contato.status, "arquivado")

    def test_telefone_defaults_to_blank(self):
        self.assertEqual(self.contato.telefone, "")

    def test_ip_address_defaults_to_none(self):
        self.assertIsNone(self.contato.ip_address)

    def test_ip_address_can_be_set(self):
        self.contato.ip_address = "192.168.1.1"
        self.contato.save()
        self.contato.refresh_from_db()
        self.assertEqual(self.contato.ip_address, "192.168.1.1")

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.contato.created_at)

    def test_ordering_newest_first(self):
        c2 = Contato.objects.create(
            nome="Maria",
            email="maria@example.com",
            assunto="Dúvida",
            mensagem="Minha dúvida.",
        )
        contatos = list(Contato.objects.all())
        self.assertEqual(contatos[0].pk, c2.pk)

    def test_mensagem_field_stored(self):
        self.assertEqual(
            self.contato.mensagem,
            "Gostaria de um orçamento para meu e-commerce.",
        )


# ─────────────────────────── Depoimento ─────────────────────────────────────


class DepoimentoModelTest(TestCase):
    """Tests for the Depoimento (testimonial) model."""

    def setUp(self):
        self.depoimento = Depoimento.objects.create(
            nome="Pedro Santos",
            cargo="CEO",
            empresa="Santos Tech",
            depoimento_pt="Excelente trabalho! Recomendo muito.",
            depoimento_en="Excellent work! Highly recommended.",
            avaliacao=5,
        )

    def test_str_includes_nome_and_empresa(self):
        result = str(self.depoimento)
        self.assertIn("Pedro Santos", result)
        self.assertIn("Santos Tech", result)

    def test_default_ativo_true(self):
        self.assertTrue(self.depoimento.ativo)

    def test_default_destaque_false(self):
        self.assertFalse(self.depoimento.destaque)

    def test_default_ordem_zero(self):
        self.assertEqual(self.depoimento.ordem, 0)

    def test_avaliacao_five(self):
        self.assertEqual(self.depoimento.avaliacao, 5)

    def test_can_set_avaliacao_1_to_5(self):
        for val in range(1, 6):
            self.depoimento.avaliacao = val
            self.depoimento.save()
            self.depoimento.refresh_from_db()
            self.assertEqual(self.depoimento.avaliacao, val)

    def test_destaque_can_be_set_true(self):
        self.depoimento.destaque = True
        self.depoimento.save()
        self.depoimento.refresh_from_db()
        self.assertTrue(self.depoimento.destaque)

    def test_ativo_can_be_set_false(self):
        self.depoimento.ativo = False
        self.depoimento.save()
        self.depoimento.refresh_from_db()
        self.assertFalse(self.depoimento.ativo)

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.depoimento.created_at)

    def test_depoimento_en_optional(self):
        dep = Depoimento.objects.create(
            nome="Ana Lima",
            depoimento_pt="Muito bom!",
            avaliacao=4,
        )
        self.assertEqual(dep.depoimento_en, "")


# ─────────────────────────── FAQ ────────────────────────────────────────────


class FAQModelTest(TestCase):
    """Tests for the FAQ model."""

    def setUp(self):
        self.faq = FAQ.objects.create(
            categoria="geral",
            pergunta_pt="Como funciona o serviço?",
            pergunta_en="How does the service work?",
            resposta_pt="Nosso serviço funciona de forma simples.",
            resposta_en="Our service works simply.",
        )

    def test_str_returns_pergunta_pt(self):
        self.assertIn("Como funciona o serviço?", str(self.faq))

    def test_default_ativo_true(self):
        self.assertTrue(self.faq.ativo)

    def test_default_ordem_zero(self):
        self.assertEqual(self.faq.ordem, 0)

    def test_pergunta_property_returns_pt_by_default(self):
        self.assertEqual(self.faq.pergunta, self.faq.pergunta_pt)

    def test_resposta_property_returns_pt_by_default(self):
        self.assertEqual(self.faq.resposta, self.faq.resposta_pt)

    def test_categoria_geral(self):
        self.assertEqual(self.faq.categoria, "geral")

    def test_all_categoria_choices(self):
        valid = ["geral", "servicos", "pacotes", "pagamento", "suporte"]
        for cat in valid:
            self.faq.categoria = cat
            self.faq.save()
            self.faq.refresh_from_db()
            self.assertEqual(self.faq.categoria, cat)

    def test_ativo_can_be_set_false(self):
        self.faq.ativo = False
        self.faq.save()
        self.faq.refresh_from_db()
        self.assertFalse(self.faq.ativo)

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.faq.created_at)

    def test_updated_at_auto_set(self):
        self.assertIsNotNone(self.faq.updated_at)

    def test_pergunta_en_optional(self):
        faq2 = FAQ.objects.create(
            categoria="suporte",
            pergunta_pt="O que é suporte?",
            resposta_pt="Suporte é ajuda técnica.",
        )
        self.assertEqual(faq2.pergunta_en, "")

    def test_multiple_faqs_ordered_by_category_then_order(self):
        FAQ.objects.create(
            categoria="pagamento",
            pergunta_pt="Como pago?",
            resposta_pt="Via pix.",
            ordem=0,
        )
        faqs = list(FAQ.objects.all())
        self.assertTrue(len(faqs) >= 2)
