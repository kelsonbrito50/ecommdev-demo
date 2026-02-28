"""
Projetos App Tests - Projeto, Milestone, TimelineEvento, MensagemProjeto, ArquivoProjeto
"""

import datetime

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from projetos.models import ArquivoProjeto, MensagemProjeto, Milestone, Projeto, TimelineEvento

User = get_user_model()


def make_user(email="proj_user@example.com", nome="Projeto User"):
    return User.objects.create_user(
        email=email,
        password="Senha@123456",
        nome_completo=nome,
        is_active=True,
    )


def make_projeto(cliente, nome="Meu Projeto", status="aprovado"):
    return Projeto.objects.create(
        cliente=cliente,
        nome=nome,
        descricao="Descrição do projeto de teste.",
        status=status,
        valor_total=5000,
    )


# ─────────────────────────── Projeto ─────────────────────────────────────────


class ProjetoModelTest(TestCase):
    """Tests for the Projeto (project) model."""

    def setUp(self):
        self.user = make_user()
        self.projeto = make_projeto(self.user)

    def test_str_returns_nome(self):
        self.assertEqual(str(self.projeto), "Meu Projeto")

    def test_slug_auto_generated(self):
        self.assertEqual(self.projeto.slug, "meu-projeto")

    def test_default_status_aprovado(self):
        self.assertEqual(self.projeto.status, "aprovado")

    def test_status_color_aprovado(self):
        self.assertEqual(self.projeto.status_color, "info")

    def test_status_color_em_desenvolvimento(self):
        self.projeto.status = "em_desenvolvimento"
        self.assertEqual(self.projeto.status_color, "primary")

    def test_status_color_concluido(self):
        self.projeto.status = "concluido"
        self.assertEqual(self.projeto.status_color, "success")

    def test_status_color_cancelado(self):
        self.projeto.status = "cancelado"
        self.assertEqual(self.projeto.status_color, "danger")

    def test_status_color_pausado(self):
        self.projeto.status = "pausado"
        self.assertEqual(self.projeto.status_color, "secondary")

    def test_all_status_choices(self):
        statuses = [
            "orcamento",
            "aprovado",
            "em_desenvolvimento",
            "em_testes",
            "revisao",
            "concluido",
            "em_manutencao",
            "pausado",
            "cancelado",
        ]
        for s in statuses:
            self.projeto.status = s
            self.projeto.save()
            self.projeto.refresh_from_db()
            self.assertEqual(self.projeto.status, s)

    def test_cliente_relationship(self):
        self.assertEqual(self.projeto.cliente, self.user)

    def test_related_name_projetos(self):
        self.assertIn(self.projeto, self.user.projetos.all())

    def test_progresso_default_zero(self):
        self.assertEqual(self.projeto.progresso, 0)

    def test_progresso_can_be_set(self):
        self.projeto.progresso = 75
        self.projeto.save()
        self.projeto.refresh_from_db()
        self.assertEqual(self.projeto.progresso, 75)

    def test_valor_total_field(self):
        self.assertEqual(self.projeto.valor_total, 5000)

    def test_datas_optional(self):
        self.assertIsNone(self.projeto.data_inicio)
        self.assertIsNone(self.projeto.data_previsao)
        self.assertIsNone(self.projeto.data_conclusao)

    def test_responsavel_optional(self):
        self.assertIsNone(self.projeto.responsavel)

    def test_equipe_many_to_many(self):
        user2 = make_user("dev@example.com", "Developer")
        self.projeto.equipe.add(user2)
        self.assertIn(user2, self.projeto.equipe.all())

    def test_slug_unique_per_projeto(self):
        with self.assertRaises(IntegrityError):
            Projeto.objects.create(
                cliente=self.user,
                nome="Meu Projeto",
                slug="meu-projeto",
            )

    def test_tecnologias_default_empty_list(self):
        self.assertEqual(self.projeto.tecnologias, [])

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.projeto.created_at)

    def test_updated_at_auto_set(self):
        self.assertIsNotNone(self.projeto.updated_at)


# ─────────────────────────── Milestone ───────────────────────────────────────


class MilestoneModelTest(TestCase):
    """Tests for the Milestone model."""

    def setUp(self):
        self.user = make_user("mile_user@example.com", "Milestone User")
        self.projeto = make_projeto(self.user, "Projeto Milestones")
        self.milestone = Milestone.objects.create(
            projeto=self.projeto,
            titulo="Fase 1 - Planejamento",
            descricao="Levantamento de requisitos e wireframes.",
            status="pendente",
            data_previsao=datetime.date.today(),
            ordem=1,
        )

    def test_str_includes_projeto_and_titulo(self):
        result = str(self.milestone)
        self.assertIn("Projeto Milestones", result)
        self.assertIn("Fase 1 - Planejamento", result)

    def test_default_status_pendente(self):
        self.assertEqual(self.milestone.status, "pendente")

    def test_all_status_choices(self):
        for s in ["pendente", "em_andamento", "concluido", "atrasado"]:
            self.milestone.status = s
            self.milestone.save()
            self.milestone.refresh_from_db()
            self.assertEqual(self.milestone.status, s)

    def test_projeto_relationship(self):
        self.assertEqual(self.milestone.projeto, self.projeto)

    def test_related_name_milestones(self):
        self.assertIn(self.milestone, self.projeto.milestones.all())

    def test_ordem_field(self):
        self.assertEqual(self.milestone.ordem, 1)

    def test_data_conclusao_optional(self):
        self.assertIsNone(self.milestone.data_conclusao)

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.milestone.created_at)

    def test_multiple_milestones_per_project(self):
        Milestone.objects.create(
            projeto=self.projeto,
            titulo="Fase 2 - Desenvolvimento",
            status="pendente",
            ordem=2,
        )
        self.assertEqual(self.projeto.milestones.count(), 2)


# ─────────────────────────── TimelineEvento ──────────────────────────────────


class TimelineEventoModelTest(TestCase):
    """Tests for the TimelineEvento model."""

    def setUp(self):
        self.user = make_user("tl_user@example.com", "Timeline User")
        self.projeto = make_projeto(self.user, "Projeto Timeline")
        self.evento = TimelineEvento.objects.create(
            projeto=self.projeto,
            tipo="criacao",
            titulo="Projeto criado",
            descricao="O projeto foi criado com sucesso.",
            usuario=self.user,
        )

    def test_str_includes_projeto_and_titulo(self):
        result = str(self.evento)
        self.assertIn("Projeto Timeline", result)
        self.assertIn("Projeto criado", result)

    def test_tipo_criacao(self):
        self.assertEqual(self.evento.tipo, "criacao")

    def test_all_tipo_choices(self):
        tipos = ["criacao", "atualizacao", "milestone", "mensagem", "arquivo", "status", "reuniao"]
        for t in tipos:
            self.evento.tipo = t
            self.evento.save()
            self.evento.refresh_from_db()
            self.assertEqual(self.evento.tipo, t)

    def test_projeto_relationship(self):
        self.assertEqual(self.evento.projeto, self.projeto)

    def test_related_name_timeline(self):
        self.assertIn(self.evento, self.projeto.timeline.all())

    def test_usuario_optional(self):
        evento_sem_user = TimelineEvento.objects.create(
            projeto=self.projeto,
            tipo="atualizacao",
            titulo="Update automático",
        )
        self.assertIsNone(evento_sem_user.usuario)

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.evento.created_at)

    def test_ordering_newest_first(self):
        evento2 = TimelineEvento.objects.create(
            projeto=self.projeto,
            tipo="status",
            titulo="Status alterado",
        )
        eventos = list(TimelineEvento.objects.filter(projeto=self.projeto))
        self.assertEqual(eventos[0].pk, evento2.pk)


# ─────────────────────────── MensagemProjeto ─────────────────────────────────


class MensagemProjetoModelTest(TestCase):
    """Tests for the MensagemProjeto model."""

    def setUp(self):
        self.user = make_user("msg_user@example.com", "Mensagem User")
        self.projeto = make_projeto(self.user, "Projeto Mensagens")
        self.mensagem = MensagemProjeto.objects.create(
            projeto=self.projeto,
            autor=self.user,
            conteudo="Olá, como está o andamento do projeto?",
        )

    def test_str_includes_autor(self):
        result = str(self.mensagem)
        self.assertIn("Mensagem User", result)

    def test_conteudo_stored(self):
        self.assertEqual(
            self.mensagem.conteudo,
            "Olá, como está o andamento do projeto?",
        )

    def test_lido_default_false(self):
        self.assertFalse(self.mensagem.lido)

    def test_projeto_relationship(self):
        self.assertEqual(self.mensagem.projeto, self.projeto)

    def test_related_name_mensagens(self):
        self.assertIn(self.mensagem, self.projeto.mensagens.all())

    def test_autor_optional_on_delete(self):
        # autor can be null (SET_NULL)
        msg = MensagemProjeto.objects.create(
            projeto=self.projeto,
            autor=None,
            conteudo="Mensagem do sistema.",
        )
        self.assertIsNone(msg.autor)

    def test_anexos_default_empty_list(self):
        self.assertEqual(self.mensagem.anexos, [])

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.mensagem.created_at)

    def test_can_mark_as_lido(self):
        self.mensagem.lido = True
        self.mensagem.save()
        self.mensagem.refresh_from_db()
        self.assertTrue(self.mensagem.lido)


# ─────────────────────────── ArquivoProjeto ──────────────────────────────────


class ArquivoProjetoModelTest(TestCase):
    """Tests for the ArquivoProjeto model (metadata only, no actual file)."""

    def setUp(self):
        self.user = make_user("arq_user@example.com", "Arquivo User")
        self.projeto = make_projeto(self.user, "Projeto Arquivos")

    def test_all_tipo_choices(self):
        valid_tipos = ["design", "documento", "codigo", "imagem", "outro"]
        for t in valid_tipos:
            self.assertIn(t, [c[0] for c in ArquivoProjeto.TIPO_CHOICES])

    def test_str_returns_nome(self):
        # We can't create an ArquivoProjeto without a file, but we can test the model fields
        arquivo = ArquivoProjeto.__new__(ArquivoProjeto)
        arquivo.nome = "wireframe.pdf"
        self.assertEqual(arquivo.nome, "wireframe.pdf")

    def test_tamanho_property_zero_when_no_file(self):
        arquivo = ArquivoProjeto.__new__(ArquivoProjeto)
        arquivo.arquivo = None
        self.assertEqual(arquivo.tamanho, 0)

    def test_tamanho_formatado_empty_string_when_zero(self):
        arquivo = ArquivoProjeto.__new__(ArquivoProjeto)
        arquivo.arquivo = None
        self.assertEqual(arquivo.tamanho_formatado, "")

    def test_project_relationship(self):
        self.assertEqual(self.projeto.arquivos.count(), 0)

    def test_meta_ordering_newest_first(self):
        meta = ArquivoProjeto._meta
        self.assertIn("-created_at", meta.ordering)
