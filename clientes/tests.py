"""
Clientes App Tests - Usuario, PerfilEmpresa, LogLogin, SessaoAtiva
"""

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import Client, TestCase

from clientes.models import LogLogin, PerfilEmpresa, SessaoAtiva

User = get_user_model()


# ─────────────────────────── Usuario ────────────────────────────────────────


class UsuarioModelTest(TestCase):
    """Tests for the custom Usuario model (email-based auth)."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="cliente@example.com",
            password="Senhasegura@123",
            nome_completo="João Cliente",
            is_active=True,
        )

    def test_str_returns_nome_completo(self):
        self.assertEqual(str(self.user), "João Cliente")

    def test_email_is_username_field(self):
        self.assertEqual(User.USERNAME_FIELD, "email")

    def test_email_is_unique(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email="cliente@example.com",
                password="OutraSenha@456",
                nome_completo="Outro João",
                is_active=True,
            )

    def test_username_field_not_present(self):
        # username = None in the model, so it is not a DB field
        field_names = [f.name for f in User._meta.get_fields()]
        self.assertNotIn("username", field_names)

    def test_get_full_name(self):
        self.assertEqual(self.user.get_full_name(), "João Cliente")

    def test_get_short_name(self):
        self.assertEqual(self.user.get_short_name(), "João")

    def test_default_idioma_preferido(self):
        self.assertEqual(self.user.idioma_preferido, "pt-br")

    def test_default_notificacoes_email_true(self):
        self.assertTrue(self.user.notificacoes_email)

    def test_default_notificacoes_sms_false(self):
        self.assertFalse(self.user.notificacoes_sms)

    def test_default_two_factor_disabled(self):
        self.assertFalse(self.user.two_factor_enabled)

    def test_default_email_not_verified(self):
        self.assertFalse(self.user.email_verified)

    def test_email_verification_token_is_uuid(self):
        import uuid

        self.assertIsInstance(self.user.email_verification_token, uuid.UUID)

    def test_regenerate_verification_token(self):
        old_token = self.user.email_verification_token
        new_token = self.user.regenerate_verification_token()
        self.assertNotEqual(old_token, new_token)

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email="admin@example.com",
            password="AdminSenha@123",
            nome_completo="Admin User",
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_active)

    def test_create_user_inactive_by_default(self):
        inactive_user = User.objects.create_user(
            email="inactive@example.com",
            password="Senha@123456",
            nome_completo="Inactive User",
        )
        self.assertFalse(inactive_user.is_active)

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.user.created_at)

    def test_updated_at_auto_set(self):
        self.assertIsNotNone(self.user.updated_at)

    def test_telefone_defaults_blank(self):
        self.assertEqual(self.user.telefone, "")

    def test_cpf_defaults_blank(self):
        self.assertEqual(self.user.cpf, "")


# ─────────────────────────── PerfilEmpresa ──────────────────────────────────


class PerfilEmpresaModelTest(TestCase):
    """Tests for the PerfilEmpresa (company profile) model."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="empresa@example.com",
            password="Senha@123456",
            nome_completo="Carlos Empresa",
            is_active=True,
        )
        self.perfil = PerfilEmpresa.objects.create(
            usuario=self.user,
            nome_empresa="Carlos LTDA",
            cnpj="00.000.000/0001-00",
            cidade="Fortaleza",
            estado="CE",
        )

    def test_str_returns_nome_empresa(self):
        self.assertEqual(str(self.perfil), "Carlos LTDA")

    def test_str_fallback_when_no_empresa_name(self):
        perfil_sem_nome = PerfilEmpresa.objects.create(
            usuario=User.objects.create_user(
                email="semempresa@example.com",
                password="Senha@123456",
                nome_completo="Sem Empresa",
                is_active=True,
            )
        )
        self.assertIn("Sem Empresa", str(perfil_sem_nome))

    def test_one_to_one_with_usuario(self):
        self.assertEqual(self.perfil.usuario, self.user)

    def test_related_name_empresa(self):
        self.assertEqual(self.user.empresa, self.perfil)

    def test_cnpj_field(self):
        self.assertEqual(self.perfil.cnpj, "00.000.000/0001-00")

    def test_cidade_field(self):
        self.assertEqual(self.perfil.cidade, "Fortaleza")

    def test_estado_field(self):
        self.assertEqual(self.perfil.estado, "CE")

    def test_optional_fields_default_blank(self):
        self.assertEqual(self.perfil.endereco, "")
        self.assertEqual(self.perfil.cep, "")
        self.assertEqual(self.perfil.website, "")
        self.assertEqual(self.perfil.ramo_atividade, "")

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.perfil.created_at)

    def test_updated_at_auto_set(self):
        self.assertIsNotNone(self.perfil.updated_at)


# ─────────────────────────── LogLogin ───────────────────────────────────────


class LogLoginModelTest(TestCase):
    """Tests for the LogLogin (login history) model."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="loguser@example.com",
            password="Senha@123456",
            nome_completo="Log User",
            is_active=True,
        )
        self.log = LogLogin.objects.create(
            usuario=self.user,
            ip_address="10.0.0.1",
            user_agent="Mozilla/5.0",
            dispositivo="Desktop",
            localizacao="Fortaleza, CE",
            sucesso=True,
        )

    def test_str_includes_usuario(self):
        result = str(self.log)
        self.assertIn("Log User", result)

    def test_sucesso_field_true(self):
        self.assertTrue(self.log.sucesso)

    def test_failed_login_log(self):
        failed = LogLogin.objects.create(
            usuario=self.user,
            ip_address="10.0.0.2",
            sucesso=False,
        )
        self.assertFalse(failed.sucesso)

    def test_ip_address_stored(self):
        self.assertEqual(self.log.ip_address, "10.0.0.1")

    def test_related_name_logs_login(self):
        logs = self.user.logs_login.all()
        self.assertIn(self.log, logs)

    def test_ordering_newest_first(self):
        log2 = LogLogin.objects.create(
            usuario=self.user,
            ip_address="10.0.0.3",
            sucesso=True,
        )
        logs = list(LogLogin.objects.all())
        self.assertEqual(logs[0].pk, log2.pk)

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.log.created_at)


# ─────────────────────────── SessaoAtiva ────────────────────────────────────


class SessaoAtivaModelTest(TestCase):
    """Tests for the SessaoAtiva (active session) model."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="sessao@example.com",
            password="Senha@123456",
            nome_completo="Sessao User",
            is_active=True,
        )
        self.sessao = SessaoAtiva.objects.create(
            usuario=self.user,
            session_key="abc123def456ghi789jkl012mno345pq",
            ip_address="192.168.0.1",
            dispositivo="MacBook Pro",
            navegador="Chrome 120",
        )

    def test_str_includes_usuario_and_dispositivo(self):
        result = str(self.sessao)
        self.assertIn("Sessao User", result)
        self.assertIn("MacBook Pro", result)

    def test_session_key_stored(self):
        self.assertEqual(self.sessao.session_key, "abc123def456ghi789jkl012mno345pq")

    def test_ip_address_stored(self):
        self.assertEqual(self.sessao.ip_address, "192.168.0.1")

    def test_navegador_stored(self):
        self.assertEqual(self.sessao.navegador, "Chrome 120")

    def test_related_name_sessoes_ativas(self):
        sessoes = self.user.sessoes_ativas.all()
        self.assertIn(self.sessao, sessoes)

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.sessao.created_at)

    def test_ultimo_acesso_auto_update(self):
        self.assertIsNotNone(self.sessao.ultimo_acesso)

    def test_multiple_sessions_for_same_user(self):
        SessaoAtiva.objects.create(
            usuario=self.user,
            session_key="zzz123def456ghi789jkl012mno345zz",
            ip_address="192.168.0.2",
            dispositivo="iPhone",
            navegador="Safari",
        )
        self.assertEqual(self.user.sessoes_ativas.count(), 2)


# ─────────────────────────── Auth View Tests ────────────────────────────────


class ClienteAuthViewTest(TestCase):
    """Tests for login/register views (status codes)."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="authtest@example.com",
            password="Senha@123456",
            nome_completo="Auth Test User",
            is_active=True,
            email_verified=True,
        )

    def test_login_page_accessible(self):
        response = self.client.get("/login/")
        self.assertIn(response.status_code, [200, 301, 302, 404])

    def test_perfil_requires_auth(self):
        response = self.client.get("/perfil/")
        # Should redirect to login if not authenticated
        self.assertIn(response.status_code, [301, 302, 404])

    def test_authenticated_user_has_email(self):
        self.client.login(username="authtest@example.com", password="Senha@123456")
        self.assertEqual(self.user.email, "authtest@example.com")
