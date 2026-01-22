"""API v1 views."""
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .serializers import (
    ServicoSerializer, PacoteSerializer, CaseSerializer,
    OrcamentoSerializer, ProjetoSerializer, TicketSerializer, FaturaSerializer,
    ClienteSerializer, ContatoSerializer, NotificacaoSerializer
)
from servicos.models import Servico
from pacotes.models import Pacote
from portfolio.models import Case
from orcamentos.models import Orcamento
from projetos.models import Projeto
from suporte.models import Ticket
from faturas.models import Fatura
from core.models import Contato
from notificacoes.models import Notificacao


class ServicoViewSet(viewsets.ReadOnlyModelViewSet):
    """Public service catalog."""
    queryset = Servico.objects.filter(ativo=True)
    serializer_class = ServicoSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


class PacoteViewSet(viewsets.ReadOnlyModelViewSet):
    """Public pricing packages."""
    queryset = Pacote.objects.filter(ativo=True)
    serializer_class = PacoteSerializer
    permission_classes = [AllowAny]
    lookup_field = 'tipo'


class CaseViewSet(viewsets.ReadOnlyModelViewSet):
    """Public portfolio cases."""
    queryset = Case.objects.filter(ativo=True)
    serializer_class = CaseSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


class OrcamentoViewSet(viewsets.ModelViewSet):
    """Quote requests - create public, list for authenticated users."""
    serializer_class = OrcamentoSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return Orcamento.objects.all()
            return Orcamento.objects.filter(cliente=self.request.user)
        return Orcamento.objects.none()

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        ip = self.request.META.get('REMOTE_ADDR')
        if self.request.user.is_authenticated:
            serializer.save(cliente=self.request.user, ip_address=ip)
        else:
            serializer.save(ip_address=ip)


class ProjetoViewSet(viewsets.ReadOnlyModelViewSet):
    """Client projects."""
    serializer_class = ProjetoSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Projeto.objects.all()
        return Projeto.objects.filter(cliente=self.request.user)


class TicketViewSet(viewsets.ModelViewSet):
    """Support tickets."""
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'numero'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(cliente=self.request.user)

    def perform_create(self, serializer):
        serializer.save(cliente=self.request.user)

    @action(detail=True, methods=['post'])
    def responder(self, request, numero=None):
        ticket = self.get_object()
        conteudo = request.data.get('conteudo')
        if conteudo:
            ticket.respostas.create(
                autor=request.user,
                conteudo=conteudo
            )
            return Response({'status': 'resposta adicionada'})
        return Response({'error': 'conteudo é obrigatório'}, status=400)


class FaturaViewSet(viewsets.ReadOnlyModelViewSet):
    """Client invoices."""
    serializer_class = FaturaSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'numero'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Fatura.objects.all()
        return Fatura.objects.filter(cliente=self.request.user)


class ClienteProfileView(generics.RetrieveUpdateAPIView):
    """Client profile."""
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ContatoCreateView(generics.CreateAPIView):
    """Public contact form."""
    serializer_class = ContatoSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        ip = self.request.META.get('REMOTE_ADDR')
        serializer.save(ip_address=ip)


class NotificacaoListView(generics.ListAPIView):
    """User notifications."""
    serializer_class = NotificacaoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notificacao.objects.filter(usuario=self.request.user)


class NotificacaoMarcarLidaView(APIView):
    """Mark notification as read."""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        notificacao = get_object_or_404(
            Notificacao,
            pk=pk,
            usuario=request.user
        )
        notificacao.lida = True
        notificacao.save()
        return Response({'status': 'marcada como lida'})
