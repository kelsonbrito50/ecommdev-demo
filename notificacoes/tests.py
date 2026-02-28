"""
Notificacoes App Tests - Notificacao, LogEmail, ConfiguracaoNotificacao
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from notificacoes.models import Notificacao, LogEmail, ConfiguracaoNotificacao

User = get_user_model()


def make_user(email='notif_user@example.com', nome='Notif User'):
    return User.objects.create_user(
        email=email,
        password='Senha@123456',
        nome_completo=nome,
        is_active=True,
    )


# ─────────────────────────── Notificacao ─────────────────────────────────────

class NotificacaoModelTest(TestCase):
    """Tests for the Notificacao model."""

    def setUp(self):
        self.user = make_user()
        self.notificacao = Notificacao.objects.create(
            usuario=self.user,
            tipo='info',
            categoria='projeto',
            titulo='Projeto atualizado',
            mensagem='Seu projeto foi atualizado com sucesso.',
            url='/dashboard/projetos/meu-projeto/',
        )

    def test_str_includes_usuario_and_titulo(self):
        result = str(self.notificacao)
        self.assertIn('Notif User', result)
        self.assertIn('Projeto atualizado', result)

    def test_tipo_info(self):
        self.assertEqual(self.notificacao.tipo, 'info')

    def test_all_tipo_choices(self):
        for tipo in ['info', 'sucesso', 'aviso', 'erro']:
            self.notificacao.tipo = tipo
            self.notificacao.save()
            self.notificacao.refresh_from_db()
            self.assertEqual(self.notificacao.tipo, tipo)

    def test_categoria_projeto(self):
        self.assertEqual(self.notificacao.categoria, 'projeto')

    def test_all_categoria_choices(self):
        categorias = ['projeto', 'orcamento', 'fatura', 'ticket', 'sistema', 'mensagem']
        for cat in categorias:
            self.notificacao.categoria = cat
            self.notificacao.save()
            self.notificacao.refresh_from_db()
            self.assertEqual(self.notificacao.categoria, cat)

    def test_titulo_field(self):
        self.assertEqual(self.notificacao.titulo, 'Projeto atualizado')

    def test_mensagem_field(self):
        self.assertIn('atualizado com sucesso', self.notificacao.mensagem)

    def test_url_field(self):
        self.assertEqual(self.notificacao.url, '/dashboard/projetos/meu-projeto/')

    def test_default_lida_false(self):
        self.assertFalse(self.notificacao.lida)

    def test_can_mark_as_lida(self):
        self.notificacao.lida = True
        self.notificacao.save()
        self.notificacao.refresh_from_db()
        self.assertTrue(self.notificacao.lida)

    def test_usuario_relationship(self):
        self.assertEqual(self.notificacao.usuario, self.user)

    def test_related_name_notificacoes(self):
        self.assertIn(self.notificacao, self.user.notificacoes.all())

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.notificacao.created_at)

    def test_ordering_newest_first(self):
        n2 = Notificacao.objects.create(
            usuario=self.user,
            tipo='sucesso',
            categoria='fatura',
            titulo='Pagamento confirmado',
            mensagem='Seu pagamento foi confirmado.',
        )
        notificacoes = list(Notificacao.objects.filter(usuario=self.user))
        self.assertEqual(notificacoes[0].pk, n2.pk)

    def test_url_optional(self):
        n = Notificacao.objects.create(
            usuario=self.user,
            tipo='sistema',
            categoria='sistema',
            titulo='Manutenção',
            mensagem='Manutenção programada.',
        )
        self.assertEqual(n.url, '')

    def test_multiple_notificacoes_per_user(self):
        Notificacao.objects.create(
            usuario=self.user,
            titulo='Segunda notificação',
            mensagem='Mensagem.',
        )
        self.assertEqual(self.user.notificacoes.count(), 2)


# ─────────────────────────── LogEmail ────────────────────────────────────────

class LogEmailModelTest(TestCase):
    """Tests for the LogEmail model."""

    def setUp(self):
        self.log = LogEmail.objects.create(
            destinatario='cliente@example.com',
            tipo='boas_vindas',
            assunto='Bem-vindo ao ECOMMDEV!',
            conteudo='<p>Olá! Bem-vindo à nossa plataforma.</p>',
            status='enviado',
        )

    def test_str_includes_tipo_and_destinatario(self):
        result = str(self.log)
        self.assertIn('boas_vindas', result)
        self.assertIn('cliente@example.com', result)

    def test_tipo_boas_vindas(self):
        self.assertEqual(self.log.tipo, 'boas_vindas')

    def test_all_tipo_choices(self):
        tipos = [
            'orcamento_confirmacao', 'orcamento_aprovado', 'projeto_atualizacao',
            'fatura_nova', 'fatura_vencimento', 'pagamento_confirmado',
            'ticket_criado', 'ticket_resposta', 'boas_vindas', 'reset_senha', 'newsletter',
        ]
        for i, tipo in enumerate(tipos):
            log = LogEmail.objects.create(
                destinatario=f'test{i}@example.com',
                tipo=tipo,
                assunto=f'Assunto {i}',
            )
            self.assertEqual(log.tipo, tipo)

    def test_status_enviado(self):
        self.assertEqual(self.log.status, 'enviado')

    def test_all_status_choices(self):
        for s in ['enviado', 'falha', 'pendente']:
            self.log.status = s
            self.log.save()
            self.log.refresh_from_db()
            self.assertEqual(self.log.status, s)

    def test_default_status_pendente(self):
        log2 = LogEmail.objects.create(
            destinatario='pending@example.com',
            tipo='newsletter',
            assunto='Newsletter Mensal',
        )
        self.assertEqual(log2.status, 'pendente')

    def test_destinatario_field(self):
        self.assertEqual(self.log.destinatario, 'cliente@example.com')

    def test_assunto_field(self):
        self.assertEqual(self.log.assunto, 'Bem-vindo ao ECOMMDEV!')

    def test_conteudo_field(self):
        self.assertIn('Bem-vindo', self.log.conteudo)

    def test_erro_default_blank(self):
        self.assertEqual(self.log.erro, '')

    def test_tentativas_default_zero(self):
        self.assertEqual(self.log.tentativas, 0)

    def test_enviado_at_optional(self):
        self.assertIsNone(self.log.enviado_at)

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.log.created_at)

    def test_ordering_newest_first(self):
        log2 = LogEmail.objects.create(
            destinatario='newer@example.com',
            tipo='reset_senha',
            assunto='Reset de senha',
        )
        logs = list(LogEmail.objects.all())
        self.assertEqual(logs[0].pk, log2.pk)


# ─────────────────────────── ConfiguracaoNotificacao ─────────────────────────

class ConfiguracaoNotificacaoModelTest(TestCase):
    """Tests for the ConfiguracaoNotificacao model."""

    def setUp(self):
        self.user = make_user('cfg_notif@example.com', 'Config Notif User')
        self.config = ConfiguracaoNotificacao.objects.create(
            usuario=self.user,
        )

    def test_str_includes_usuario(self):
        result = str(self.config)
        self.assertIn('Config Notif User', result)

    def test_one_to_one_with_user(self):
        self.assertEqual(self.config.usuario, self.user)

    def test_related_name_config_notificacoes(self):
        self.assertEqual(self.user.config_notificacoes, self.config)

    def test_default_email_atualizacao_projeto_true(self):
        self.assertTrue(self.config.email_atualizacao_projeto)

    def test_default_email_nova_fatura_true(self):
        self.assertTrue(self.config.email_nova_fatura)

    def test_default_email_resposta_ticket_true(self):
        self.assertTrue(self.config.email_resposta_ticket)

    def test_default_email_newsletter_false(self):
        self.assertFalse(self.config.email_newsletter)

    def test_default_email_marketing_false(self):
        self.assertFalse(self.config.email_marketing)

    def test_default_push_atualizacao_projeto_true(self):
        self.assertTrue(self.config.push_atualizacao_projeto)

    def test_default_push_nova_fatura_true(self):
        self.assertTrue(self.config.push_nova_fatura)

    def test_default_push_resposta_ticket_true(self):
        self.assertTrue(self.config.push_resposta_ticket)

    def test_can_disable_email_newsletter(self):
        self.config.email_newsletter = False
        self.config.save()
        self.config.refresh_from_db()
        self.assertFalse(self.config.email_newsletter)

    def test_can_enable_email_marketing(self):
        self.config.email_marketing = True
        self.config.save()
        self.config.refresh_from_db()
        self.assertTrue(self.config.email_marketing)

    def test_updated_at_auto_set(self):
        self.assertIsNotNone(self.config.updated_at)

    def test_only_one_config_per_user(self):
        with self.assertRaises(Exception):
            ConfiguracaoNotificacao.objects.create(usuario=self.user)
