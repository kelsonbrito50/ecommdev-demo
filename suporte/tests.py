"""
Suporte App Tests - Ticket, RespostaTicket, AvaliacaoTicket
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from suporte.models import Ticket, RespostaTicket, AvaliacaoTicket

User = get_user_model()


def make_user(email='suporte_user@example.com', nome='Suporte User'):
    return User.objects.create_user(
        email=email,
        password='Senha@123456',
        nome_completo=nome,
        is_active=True,
    )


def make_ticket(cliente, assunto='Bug no site', categoria='tecnico', **kwargs):
    return Ticket.objects.create(
        cliente=cliente,
        assunto=assunto,
        descricao='Ao clicar no botão comprar, ocorre um erro 500.',
        categoria=categoria,
        prioridade='alta',
        **kwargs,
    )


# ─────────────────────────── Ticket ──────────────────────────────────────────

class TicketModelTest(TestCase):
    """Tests for the Ticket (support ticket) model."""

    def setUp(self):
        self.user = make_user()
        self.ticket = make_ticket(self.user)

    def test_str_includes_numero_and_assunto(self):
        result = str(self.ticket)
        self.assertIn('TKT-', result)
        self.assertIn('Bug no site', result)

    def test_numero_auto_generated(self):
        self.assertTrue(self.ticket.numero.startswith('TKT-'))

    def test_numero_format(self):
        import re
        self.assertRegex(self.ticket.numero, r'^TKT-\d{4}-\d{4}$')

    def test_default_status_aberto(self):
        self.assertEqual(self.ticket.status, 'aberto')

    def test_default_prioridade_alta(self):
        self.assertEqual(self.ticket.prioridade, 'alta')

    def test_all_status_choices(self):
        statuses = ['aberto', 'em_atendimento', 'aguardando_cliente', 'resolvido', 'fechado']
        for s in statuses:
            self.ticket.status = s
            self.ticket.save()
            self.ticket.refresh_from_db()
            self.assertEqual(self.ticket.status, s)

    def test_all_prioridade_choices(self):
        for p in ['baixa', 'media', 'alta', 'urgente']:
            self.ticket.prioridade = p
            self.ticket.save()
            self.ticket.refresh_from_db()
            self.assertEqual(self.ticket.prioridade, p)

    def test_all_categoria_choices(self):
        for cat in ['tecnico', 'duvida', 'solicitacao', 'financeiro', 'outro']:
            self.ticket.categoria = cat
            self.ticket.save()
            self.ticket.refresh_from_db()
            self.assertEqual(self.ticket.categoria, cat)

    def test_cliente_relationship(self):
        self.assertEqual(self.ticket.cliente, self.user)

    def test_related_name_tickets(self):
        self.assertIn(self.ticket, self.user.tickets.all())

    def test_projeto_optional(self):
        self.assertIsNone(self.ticket.projeto)

    def test_atendente_optional(self):
        self.assertIsNone(self.ticket.atendente)

    def test_anexos_default_empty_list(self):
        self.assertEqual(self.ticket.anexos, [])

    def test_data_primeira_resposta_optional(self):
        self.assertIsNone(self.ticket.data_primeira_resposta)

    def test_data_resolucao_optional(self):
        self.assertIsNone(self.ticket.data_resolucao)

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.ticket.created_at)

    def test_updated_at_auto_set(self):
        self.assertIsNotNone(self.ticket.updated_at)

    def test_sequential_numero_generation(self):
        ticket2 = make_ticket(self.user, assunto='Outro problema')
        self.assertNotEqual(self.ticket.numero, ticket2.numero)

    def test_atendente_can_be_set(self):
        atendente = make_user('atendente@example.com', 'Atendente')
        atendente.is_staff = True
        atendente.save()
        self.ticket.atendente = atendente
        self.ticket.save()
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.atendente, atendente)

    def test_ordering_newest_first(self):
        ticket2 = make_ticket(self.user, assunto='Segundo ticket')
        tickets = list(Ticket.objects.all())
        self.assertEqual(tickets[0].pk, ticket2.pk)

    def test_descricao_field(self):
        self.assertIn('Ao clicar no botão comprar', self.ticket.descricao)


# ─────────────────────────── RespostaTicket ──────────────────────────────────

class RespostaTicketModelTest(TestCase):
    """Tests for the RespostaTicket model."""

    def setUp(self):
        self.user = make_user('suporte2@example.com', 'Suporte User 2')
        self.atendente = make_user('staff@example.com', 'Staff Member')
        self.ticket = make_ticket(self.user)
        self.resposta = RespostaTicket.objects.create(
            ticket=self.ticket,
            autor=self.atendente,
            conteudo='Identificamos o problema. Estamos trabalhando na solução.',
            solucao_proposta='Atualizar o plugin de pagamento para a versão 3.2.',
            interno=False,
        )

    def test_str_includes_ticket_numero_and_autor(self):
        result = str(self.resposta)
        self.assertIn(self.ticket.numero, result)
        self.assertIn('Staff Member', result)

    def test_conteudo_field(self):
        self.assertIn('Identificamos o problema', self.resposta.conteudo)

    def test_solucao_proposta_field(self):
        self.assertIn('Atualizar o plugin', self.resposta.solucao_proposta)

    def test_interno_false(self):
        self.assertFalse(self.resposta.interno)

    def test_nota_interna(self):
        nota = RespostaTicket.objects.create(
            ticket=self.ticket,
            autor=self.atendente,
            conteudo='Nota interna: cliente já relatou isso antes.',
            interno=True,
        )
        self.assertTrue(nota.interno)

    def test_ticket_relationship(self):
        self.assertEqual(self.resposta.ticket, self.ticket)

    def test_related_name_respostas(self):
        self.assertIn(self.resposta, self.ticket.respostas.all())

    def test_autor_optional_on_delete(self):
        resp = RespostaTicket.objects.create(
            ticket=self.ticket,
            autor=None,
            conteudo='Resposta do sistema.',
        )
        self.assertIsNone(resp.autor)

    def test_anexos_default_empty_list(self):
        self.assertEqual(self.resposta.anexos, [])

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.resposta.created_at)

    def test_ordering_oldest_first(self):
        resp2 = RespostaTicket.objects.create(
            ticket=self.ticket,
            autor=self.atendente,
            conteudo='Segunda resposta.',
        )
        respostas = list(RespostaTicket.objects.filter(ticket=self.ticket))
        self.assertEqual(respostas[0].pk, self.resposta.pk)

    def test_multiple_respostas_per_ticket(self):
        RespostaTicket.objects.create(
            ticket=self.ticket,
            autor=self.user,
            conteudo='Obrigado! Aguardando...',
        )
        self.assertEqual(self.ticket.respostas.count(), 2)


# ─────────────────────────── AvaliacaoTicket ─────────────────────────────────

class AvaliacaoTicketModelTest(TestCase):
    """Tests for the AvaliacaoTicket (ticket rating) model."""

    def setUp(self):
        self.user = make_user('avaliacao@example.com', 'Avaliacao User')
        self.ticket = make_ticket(self.user)
        self.avaliacao = AvaliacaoTicket.objects.create(
            ticket=self.ticket,
            nota=5,
            comentario='Excelente atendimento! Problema resolvido rapidamente.',
        )

    def test_str_includes_ticket_numero_and_nota(self):
        result = str(self.avaliacao)
        self.assertIn(self.ticket.numero, result)
        self.assertIn('5', result)
        self.assertIn('estrelas', result)

    def test_nota_field(self):
        self.assertEqual(self.avaliacao.nota, 5)

    def test_comentario_field(self):
        self.assertIn('Excelente atendimento', self.avaliacao.comentario)

    def test_one_to_one_with_ticket(self):
        self.assertEqual(self.avaliacao.ticket, self.ticket)

    def test_related_name_avaliacao(self):
        self.assertEqual(self.ticket.avaliacao, self.avaliacao)

    def test_only_one_avaliacao_per_ticket(self):
        with self.assertRaises(Exception):
            AvaliacaoTicket.objects.create(
                ticket=self.ticket,
                nota=3,
            )

    def test_all_nota_choices(self):
        # Test each valid nota value (1-5)
        for nota in range(1, 6):
            user = make_user(f'eval{nota}@example.com', f'Eval User {nota}')
            ticket = make_ticket(user, assunto=f'Ticket nota {nota}')
            av = AvaliacaoTicket.objects.create(ticket=ticket, nota=nota)
            self.assertEqual(av.nota, nota)

    def test_comentario_optional(self):
        user2 = make_user('sem_comment@example.com', 'No Comment User')
        ticket2 = make_ticket(user2, assunto='Ticket sem comentário')
        av2 = AvaliacaoTicket.objects.create(ticket=ticket2, nota=4)
        self.assertEqual(av2.comentario, '')

    def test_created_at_auto_set(self):
        self.assertIsNotNone(self.avaliacao.created_at)


# ─────────────────────────── Suporte Views ───────────────────────────────────

class SuporteViewTest(TestCase):
    """Tests for suporte views (auth required)."""

    def setUp(self):
        self.client = Client()
        self.user = make_user('view_suporte@example.com', 'View Suporte')

    def test_ticket_list_requires_auth(self):
        response = self.client.get('/suporte/')
        self.assertIn(response.status_code, [301, 302, 404])

    def test_ticket_create_requires_auth(self):
        response = self.client.get('/suporte/novo/')
        self.assertIn(response.status_code, [301, 302, 404])
