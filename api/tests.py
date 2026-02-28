"""
API App Tests - REST API with JWT Auth
Tests all API endpoints: auth, servicos, pacotes, portfolio,
orcamentos, projetos, tickets, faturas, clientes, notificacoes, contato.
"""

import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Contato
from faturas.models import Fatura
from notificacoes.models import Notificacao
from pacotes.models import Pacote
from portfolio.models import Case
from projetos.models import Projeto
from servicos.models import Servico
from suporte.models import Ticket

User = get_user_model()

# ─────────────────────────── Helpers ─────────────────────────────────────────


def make_user(email="api_user@example.com", nome="API User", is_staff=False):
    user = User.objects.create_user(
        email=email,
        password="Senha@123456",
        nome_completo=nome,
        is_active=True,
    )
    if is_staff:
        user.is_staff = True
        user.save()
    return user


def make_servico(tipo="desenvolvimento", slug="servico-api-test", ativo=True, **kwargs):
    return Servico.objects.create(
        tipo=tipo,
        nome_pt="Desenvolvimento Web",
        nome_en="Web Development",
        slug=slug,
        descricao_curta_pt="Criamos sistemas web modernos.",
        descricao_pt="Desenvolvimento completo de sistemas web.",
        preco=Decimal("2500.00"),
        tipo_preco="apartir",
        ativo=ativo,
        **kwargs,
    )


def make_pacote(tipo="basico", ativo=True, **kwargs):
    return Pacote.objects.create(
        tipo=tipo,
        nome_pt="Pacote Básico",
        nome_en="Basic Package",
        preco=Decimal("997.00"),
        ativo=ativo,
        **kwargs,
    )


def make_case(slug="api-case", ativo=True, **kwargs):
    return Case.objects.create(
        titulo_pt="Case API Test",
        slug=slug,
        desafio_pt="Desafio do case.",
        solucao_pt="Solução do case.",
        ativo=ativo,
        **kwargs,
    )


def make_projeto(cliente, nome="API Projeto", **kwargs):
    return Projeto.objects.create(
        cliente=cliente,
        nome=nome,
        descricao="Descrição do projeto.",
        status="em_desenvolvimento",
        valor_total=5000,
        **kwargs,
    )


def make_ticket(cliente, **kwargs):
    return Ticket.objects.create(
        cliente=cliente,
        assunto="API Test Ticket",
        descricao="Descrição do ticket.",
        categoria="tecnico",
        prioridade="media",
        **kwargs,
    )


def make_fatura(cliente, **kwargs):
    return Fatura.objects.create(
        cliente=cliente,
        data_vencimento=datetime.date.today(),
        subtotal=Decimal("1000.00"),
        **kwargs,
    )


# ─────────────────────────── JWT Auth Tests ────────────────────────────────────


class JWTAuthTest(APITestCase):
    """Tests for JWT authentication endpoints."""

    def setUp(self):
        self.user = make_user("jwt_user@example.com", "JWT User")
        self.login_url = "/api/v1/auth/login/"
        self.refresh_url = "/api/v1/auth/refresh/"

    def test_login_with_valid_credentials(self):
        response = self.client.post(
            self.login_url,
            {
                "email": "jwt_user@example.com",
                "password": "Senha@123456",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_with_invalid_password(self):
        response = self.client.post(
            self.login_url,
            {
                "email": "jwt_user@example.com",
                "password": "SenhaErrada@999",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_with_nonexistent_user(self):
        response = self.client.post(
            self.login_url,
            {
                "email": "naoexiste@example.com",
                "password": "Qualquer@123",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh(self):
        # Get tokens first
        login_response = self.client.post(
            self.login_url,
            {
                "email": "jwt_user@example.com",
                "password": "Senha@123456",
            },
            format="json",
        )
        refresh_token = login_response.data["refresh"]

        # Refresh the access token
        response = self.client.post(
            self.refresh_url,
            {
                "refresh": refresh_token,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_access_protected_endpoint_without_token(self):
        response = self.client.get("/api/v1/projetos/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_protected_endpoint_with_valid_token(self):
        login_response = self.client.post(
            self.login_url,
            {
                "email": "jwt_user@example.com",
                "password": "Senha@123456",
            },
            format="json",
        )
        token = login_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get("/api/v1/projetos/")
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])

    def test_access_protected_endpoint_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer invalid.token.here")
        response = self.client.get("/api/v1/projetos/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ─────────────────────────── Servicos API ────────────────────────────────────


class ServicoAPITest(APITestCase):
    """Tests for the Servico (public) API endpoints."""

    def setUp(self):
        self.servico = make_servico()
        self.servico_inativo = make_servico(
            tipo="manutencao",
            slug="servico-inativo",
            ativo=False,
        )

    def test_list_servicos_public(self):
        response = self.client.get("/api/v1/servicos/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_servicos_returns_only_active(self):
        response = self.client.get("/api/v1/servicos/")
        slugs = [s["slug"] for s in response.data]
        self.assertIn("servico-api-test", slugs)
        self.assertNotIn("servico-inativo", slugs)

    def test_retrieve_servico_by_slug(self):
        response = self.client.get("/api/v1/servicos/servico-api-test/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nome_pt"], "Desenvolvimento Web")

    def test_retrieve_inactive_servico_returns_404(self):
        response = self.client.get("/api/v1/servicos/servico-inativo/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_servico_response_fields(self):
        response = self.client.get("/api/v1/servicos/servico-api-test/")
        expected_fields = [
            "id",
            "tipo",
            "nome_pt",
            "nome_en",
            "slug",
            "descricao_curta_pt",
            "descricao_pt",
            "recursos",
        ]
        for field in expected_fields:
            self.assertIn(field, response.data)

    def test_servico_api_is_read_only(self):
        response = self.client.post(
            "/api/v1/servicos/",
            {
                "nome_pt": "Novo Serviço",
                "tipo": "design",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


# ─────────────────────────── Pacotes API ──────────────────────────────────────


class PacoteAPITest(APITestCase):
    """Tests for the Pacote (public) API endpoints."""

    def setUp(self):
        self.pacote = make_pacote()
        self.pacote_inativo = make_pacote(tipo="completo", ativo=False)

    def test_list_pacotes_public(self):
        response = self.client.get("/api/v1/pacotes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_pacotes_returns_only_active(self):
        response = self.client.get("/api/v1/pacotes/")
        tipos = [p["tipo"] for p in response.data]
        self.assertIn("basico", tipos)
        self.assertNotIn("completo", tipos)

    def test_retrieve_pacote_by_tipo(self):
        response = self.client.get("/api/v1/pacotes/basico/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nome_pt"], "Pacote Básico")

    def test_pacote_response_fields(self):
        response = self.client.get("/api/v1/pacotes/basico/")
        expected_fields = ["id", "tipo", "nome_pt", "nome_en", "preco", "preco_final", "recursos"]
        for field in expected_fields:
            self.assertIn(field, response.data)

    def test_pacote_preco_final_without_promo(self):
        response = self.client.get("/api/v1/pacotes/basico/")
        self.assertEqual(str(response.data["preco_final"]), "997.00")

    def test_pacote_api_is_read_only(self):
        response = self.client.post(
            "/api/v1/pacotes/",
            {
                "tipo": "premium",
                "nome_pt": "Premium",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


# ─────────────────────────── Portfolio API ────────────────────────────────────


class PortfolioAPITest(APITestCase):
    """Tests for the Portfolio/Case (public) API endpoints."""

    def setUp(self):
        self.case = make_case()
        self.case_inativo = make_case(slug="case-inativo", ativo=False)

    def test_list_cases_public(self):
        response = self.client.get("/api/v1/portfolio/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_cases_returns_only_active(self):
        response = self.client.get("/api/v1/portfolio/")
        slugs = [c["slug"] for c in response.data]
        self.assertIn("api-case", slugs)
        self.assertNotIn("case-inativo", slugs)

    def test_retrieve_case_by_slug(self):
        response = self.client.get("/api/v1/portfolio/api-case/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["titulo_pt"], "Case API Test")

    def test_retrieve_inactive_case_returns_404(self):
        response = self.client.get("/api/v1/portfolio/case-inativo/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_case_response_fields(self):
        response = self.client.get("/api/v1/portfolio/api-case/")
        expected_fields = [
            "id",
            "titulo_pt",
            "titulo_en",
            "slug",
            "desafio_pt",
            "solucao_pt",
            "tecnologias",
        ]
        for field in expected_fields:
            self.assertIn(field, response.data)

    def test_portfolio_api_is_read_only(self):
        response = self.client.post(
            "/api/v1/portfolio/",
            {
                "titulo_pt": "Novo Case",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


# ─────────────────────────── Orcamento API ────────────────────────────────────


class OrcamentoAPITest(APITestCase):
    """Tests for the Orcamento API endpoints (create=public, list=auth)."""

    def setUp(self):
        self.user = make_user("orc_api@example.com", "Orcamento API User")
        self.login_url = "/api/v1/auth/login/"
        self.orcamento_url = "/api/v1/orcamentos/"
        self.orcamento_data = {
            "nome_completo": "Teste Empresa",
            "email": "empresa@test.com",
            "telefone": "(85) 99999-9999",
            "cidade": "Fortaleza",
            "estado": "CE",
            "tipo_projeto": "ecommerce",
            "descricao_projeto": "Quero uma loja virtual para produtos artesanais.",
        }

    def _get_token(self):
        response = self.client.post(
            self.login_url,
            {
                "email": "orc_api@example.com",
                "password": "Senha@123456",
            },
            format="json",
        )
        return response.data["access"]

    def test_create_orcamento_without_auth(self):
        response = self.client.post(self.orcamento_url, self.orcamento_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_orcamento_generates_numero(self):
        response = self.client.post(self.orcamento_url, self.orcamento_data, format="json")
        self.assertIn("numero", response.data)
        self.assertTrue(response.data["numero"].startswith("ORC-"))

    def test_create_orcamento_sets_status_novo(self):
        response = self.client.post(self.orcamento_url, self.orcamento_data, format="json")
        self.assertEqual(response.data["status"], "novo")

    def test_list_orcamentos_requires_auth(self):
        response = self.client.get(self.orcamento_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_orcamentos_authenticated(self):
        token = self._get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.orcamento_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_orcamento_missing_required_field(self):
        bad_data = self.orcamento_data.copy()
        del bad_data["email"]
        response = self.client.post(self.orcamento_url, bad_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# ─────────────────────────── Projetos API ─────────────────────────────────────


class ProjetoAPITest(APITestCase):
    """Tests for the Projeto API endpoints (auth required)."""

    def setUp(self):
        self.user = make_user("proj_api@example.com", "Projeto API User")
        self.other_user = make_user("other_api@example.com", "Other User")
        self.login_url = "/api/v1/auth/login/"
        self.projeto_url = "/api/v1/projetos/"
        self.projeto = make_projeto(self.user)

    def _get_token(self, email="proj_api@example.com"):
        response = self.client.post(
            self.login_url,
            {
                "email": email,
                "password": "Senha@123456",
            },
            format="json",
        )
        return response.data["access"]

    def test_list_projetos_requires_auth(self):
        response = self.client.get(self.projeto_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_projetos_authenticated(self):
        token = self._get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.projeto_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_projetos_returns_only_user_projects(self):
        # Create project for other user
        other_projeto = make_projeto(self.other_user, "Projeto Outro User", slug="projeto-outro")
        token = self._get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.projeto_url)
        slugs = [p["slug"] for p in response.data]
        self.assertIn(self.projeto.slug, slugs)
        self.assertNotIn(other_projeto.slug, slugs)

    def test_retrieve_projeto_by_slug(self):
        token = self._get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(f"{self.projeto_url}{self.projeto.slug}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nome"], "API Projeto")

    def test_projeto_response_fields(self):
        token = self._get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(f"{self.projeto_url}{self.projeto.slug}/")
        expected_fields = [
            "id",
            "nome",
            "slug",
            "status",
            "progresso",
            "milestones",
            "valor_total",
            "created_at",
        ]
        for field in expected_fields:
            self.assertIn(field, response.data)

    def test_cannot_see_other_users_projects(self):
        other_projeto = make_projeto(self.other_user, "Projeto Secreto", slug="projeto-secreto")
        token = self._get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(f"{self.projeto_url}{other_projeto.slug}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# ─────────────────────────── Tickets API ──────────────────────────────────────


class TicketAPITest(APITestCase):
    """Tests for the Ticket API endpoints (auth required)."""

    def setUp(self):
        self.user = make_user("ticket_api@example.com", "Ticket API User")
        self.login_url = "/api/v1/auth/login/"
        self.ticket_url = "/api/v1/tickets/"

    def _get_token(self):
        response = self.client.post(
            self.login_url,
            {
                "email": "ticket_api@example.com",
                "password": "Senha@123456",
            },
            format="json",
        )
        return response.data["access"]

    def _auth(self):
        token = self._get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_list_tickets_requires_auth(self):
        response = self.client.get(self.ticket_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_tickets_authenticated(self):
        self._auth()
        response = self.client.get(self.ticket_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_ticket_authenticated(self):
        self._auth()
        response = self.client.post(
            self.ticket_url,
            {
                "assunto": "Meu primeiro ticket",
                "descricao": "Descrevo aqui meu problema em detalhes.",
                "categoria": "duvida",
                "prioridade": "baixa",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_ticket_generates_numero(self):
        self._auth()
        response = self.client.post(
            self.ticket_url,
            {
                "assunto": "Ticket com número",
                "descricao": "Descrição do ticket.",
                "categoria": "tecnico",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["numero"].startswith("TKT-"))

    def test_create_ticket_sets_cliente_as_current_user(self):
        self._auth()
        response = self.client.post(
            self.ticket_url,
            {
                "assunto": "Ticket do usuário",
                "descricao": "Descrição.",
                "categoria": "outro",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        ticket = Ticket.objects.get(numero=response.data["numero"])
        self.assertEqual(ticket.cliente, self.user)

    def test_retrieve_ticket_by_numero(self):
        self._auth()
        ticket = make_ticket(self.user)
        response = self.client.get(f"{self.ticket_url}{ticket.numero}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["assunto"], "API Test Ticket")

    def test_ticket_response_includes_respostas(self):
        self._auth()
        ticket = make_ticket(self.user)
        response = self.client.get(f"{self.ticket_url}{ticket.numero}/")
        self.assertIn("respostas", response.data)
        self.assertIsInstance(response.data["respostas"], list)

    def test_create_ticket_missing_required_field(self):
        self._auth()
        response = self.client.post(
            self.ticket_url,
            {
                "assunto": "Ticket sem categoria",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_responder_ticket_action(self):
        self._auth()
        ticket = make_ticket(self.user)
        response = self.client.post(
            f"{self.ticket_url}{ticket.numero}/responder/",
            {"conteudo": "Esta é minha resposta ao ticket."},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ticket.respostas.count(), 1)


# ─────────────────────────── Faturas API ──────────────────────────────────────


class FaturaAPITest(APITestCase):
    """Tests for the Fatura API endpoints (auth required, read-only)."""

    def setUp(self):
        self.user = make_user("fatura_api@example.com", "Fatura API User")
        self.other_user = make_user("fatura_other@example.com", "Fatura Other")
        self.login_url = "/api/v1/auth/login/"
        self.fatura_url = "/api/v1/faturas/"
        self.fatura = make_fatura(self.user)

    def _get_token(self):
        response = self.client.post(
            self.login_url,
            {
                "email": "fatura_api@example.com",
                "password": "Senha@123456",
            },
            format="json",
        )
        return response.data["access"]

    def test_list_faturas_requires_auth(self):
        response = self.client.get(self.fatura_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_faturas_authenticated(self):
        token = self._get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.fatura_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_faturas_returns_only_user_faturas(self):
        other_fatura = make_fatura(self.other_user)
        token = self._get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.fatura_url)
        numeros = [f["numero"] for f in response.data]
        self.assertIn(self.fatura.numero, numeros)
        self.assertNotIn(other_fatura.numero, numeros)

    def test_retrieve_fatura_by_numero(self):
        token = self._get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(f"{self.fatura_url}{self.fatura.numero}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fatura_response_fields(self):
        token = self._get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(f"{self.fatura_url}{self.fatura.numero}/")
        expected_fields = [
            "id",
            "numero",
            "subtotal",
            "valor_total",
            "status",
            "itens",
            "pagamentos",
        ]
        for field in expected_fields:
            self.assertIn(field, response.data)

    def test_fatura_api_is_read_only(self):
        token = self._get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.post(
            self.fatura_url,
            {
                "numero": "FAKE-001",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


# ─────────────────────────── Cliente Profile API ─────────────────────────────


class ClienteProfileAPITest(APITestCase):
    """Tests for the /api/v1/clientes/me/ endpoint."""

    def setUp(self):
        self.user = make_user("profile_api@example.com", "Profile API User")
        self.login_url = "/api/v1/auth/login/"
        self.profile_url = "/api/v1/clientes/me/"

    def _get_token(self):
        response = self.client.post(
            self.login_url,
            {
                "email": "profile_api@example.com",
                "password": "Senha@123456",
            },
            format="json",
        )
        return response.data["access"]

    def test_get_profile_requires_auth(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile_authenticated(self):
        token = self._get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_returns_correct_user(self):
        token = self._get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.profile_url)
        self.assertEqual(response.data["email"], "profile_api@example.com")
        self.assertEqual(response.data["nome_completo"], "Profile API User")

    def test_profile_response_fields(self):
        token = self._get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.profile_url)
        expected_fields = ["id", "email", "nome_completo", "telefone", "created_at"]
        for field in expected_fields:
            self.assertIn(field, response.data)

    def test_profile_cpf_is_masked(self):
        self.user.cpf = "123.456.789-00"
        self.user.save()
        token = self._get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.profile_url)
        self.assertIn("cpf_masked", response.data)
        if response.data["cpf_masked"]:
            self.assertNotIn("123", response.data["cpf_masked"])
            self.assertIn("00", response.data["cpf_masked"])

    def test_update_profile_nome(self):
        token = self._get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.patch(
            self.profile_url,
            {
                "nome_completo": "Updated Name",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# ─────────────────────────── Contato API ──────────────────────────────────────


class ContatoAPITest(APITestCase):
    """Tests for the /api/v1/contato/ endpoint (public)."""

    def setUp(self):
        self.contato_url = "/api/v1/contato/"

    def test_create_contato_public(self):
        response = self.client.post(
            self.contato_url,
            {
                "nome": "Maria Contato",
                "email": "maria@contato.com",
                "assunto": "Quero saber mais sobre os serviços",
                "mensagem": "Olá, gostaria de informações sobre os pacotes disponíveis.",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_contato_missing_nome(self):
        response = self.client.post(
            self.contato_url,
            {
                "email": "sem_nome@test.com",
                "assunto": "Assunto",
                "mensagem": "Mensagem.",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contato_missing_mensagem(self):
        response = self.client.post(
            self.contato_url,
            {
                "nome": "Fulano",
                "email": "fulano@test.com",
                "assunto": "Assunto",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contato_invalid_email(self):
        response = self.client.post(
            self.contato_url,
            {
                "nome": "Fulano",
                "email": "email-invalido",
                "assunto": "Assunto",
                "mensagem": "Mensagem.",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_contato_saved_to_database(self):
        self.client.post(
            self.contato_url,
            {
                "nome": "DB Test User",
                "email": "dbtest@example.com",
                "assunto": "Teste DB",
                "mensagem": "Mensagem teste.",
            },
            format="json",
        )
        self.assertEqual(Contato.objects.filter(email="dbtest@example.com").count(), 1)


# ─────────────────────────── Notificacoes API ─────────────────────────────────


class NotificacaoAPITest(APITestCase):
    """Tests for the notificacoes API endpoints."""

    def setUp(self):
        self.user = make_user("notif_api@example.com", "Notif API User")
        self.login_url = "/api/v1/auth/login/"
        self.notif_url = "/api/v1/notificacoes/"

    def _get_token(self):
        response = self.client.post(
            self.login_url,
            {
                "email": "notif_api@example.com",
                "password": "Senha@123456",
            },
            format="json",
        )
        return response.data["access"]

    def _auth(self):
        token = self._get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def _make_notificacao(self, titulo="Test Notification"):
        return Notificacao.objects.create(
            usuario=self.user,
            tipo="info",
            categoria="sistema",
            titulo=titulo,
            mensagem="Mensagem de teste.",
        )

    def test_list_notificacoes_requires_auth(self):
        response = self.client.get(self.notif_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_notificacoes_authenticated(self):
        self._auth()
        self._make_notificacao()
        response = self.client.get(self.notif_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_shows_only_user_notifications(self):
        other_user = make_user("other_notif@example.com", "Other Notif")
        Notificacao.objects.create(
            usuario=other_user,
            titulo="Other User Notification",
            mensagem=".",
        )
        self._make_notificacao("My Notification")
        self._auth()
        response = self.client.get(self.notif_url)
        titulos = [n["titulo"] for n in response.data]
        self.assertIn("My Notification", titulos)
        self.assertNotIn("Other User Notification", titulos)

    def test_mark_notificacao_as_lida(self):
        self._auth()
        notif = self._make_notificacao()
        self.assertFalse(notif.lida)
        response = self.client.post(f"/api/v1/notificacoes/{notif.pk}/lida/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        notif.refresh_from_db()
        self.assertTrue(notif.lida)

    def test_mark_other_users_notificacao_returns_404(self):
        other_user = make_user("notif_other2@example.com", "Notif Other 2")
        other_notif = Notificacao.objects.create(
            usuario=other_user,
            titulo="Private Notification",
            mensagem=".",
        )
        self._auth()
        response = self.client.post(f"/api/v1/notificacoes/{other_notif.pk}/lida/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_notificacao_response_fields(self):
        self._auth()
        self._make_notificacao()
        response = self.client.get(self.notif_url)
        if response.data:
            notif_data = response.data[0]
            expected_fields = [
                "id",
                "tipo",
                "categoria",
                "titulo",
                "mensagem",
                "lida",
                "created_at",
            ]
            for field in expected_fields:
                self.assertIn(field, notif_data)
