"""API v1 views."""

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from faturas.models import Fatura
from notificacoes.models import Notificacao
from orcamentos.models import Orcamento
from pacotes.models import Pacote
from portfolio.models import Case
from projetos.models import Projeto
from servicos.models import Servico
from suporte.models import Ticket

from .serializers import (
    CaseSerializer,
    ClienteSerializer,
    ContatoSerializer,
    FaturaSerializer,
    NotificacaoSerializer,
    OrcamentoSerializer,
    PacoteSerializer,
    ProjetoSerializer,
    ServicoSerializer,
    TicketSerializer,
)


class ServicoViewSet(viewsets.ReadOnlyModelViewSet):
    """Public service catalog."""

    queryset = Servico.objects.filter(ativo=True)
    serializer_class = ServicoSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"
    pagination_class = None


class PacoteViewSet(viewsets.ReadOnlyModelViewSet):
    """Public pricing packages."""

    queryset = Pacote.objects.filter(ativo=True)
    serializer_class = PacoteSerializer
    permission_classes = [AllowAny]
    lookup_field = "tipo"
    pagination_class = None


class CaseViewSet(viewsets.ReadOnlyModelViewSet):
    """Public portfolio cases."""

    queryset = Case.objects.filter(ativo=True)
    serializer_class = CaseSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"
    pagination_class = None


class OrcamentoViewSet(viewsets.ModelViewSet):
    """Quote requests - create public, list for authenticated users."""

    serializer_class = OrcamentoSerializer
    pagination_class = None

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return Orcamento.objects.all()
            return Orcamento.objects.filter(cliente=self.request.user)
        return Orcamento.objects.none()

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        ip = self.request.META.get("REMOTE_ADDR")
        if self.request.user.is_authenticated:
            serializer.save(cliente=self.request.user, ip_address=ip)
        else:
            serializer.save(ip_address=ip)


class ProjetoViewSet(viewsets.ReadOnlyModelViewSet):
    """Client projects."""

    serializer_class = ProjetoSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"
    pagination_class = None

    def get_queryset(self):
        if self.request.user.is_staff:
            return Projeto.objects.all()
        return Projeto.objects.filter(cliente=self.request.user)


class TicketViewSet(viewsets.ModelViewSet):
    """Support tickets."""

    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "numero"
    pagination_class = None

    def get_queryset(self):
        if self.request.user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(cliente=self.request.user)

    def perform_create(self, serializer):
        serializer.save(cliente=self.request.user)

    RESPOSTA_MAX_LENGTH = 10_000  # characters — prevents DoS via oversized payloads

    @action(detail=True, methods=["post"])
    def responder(self, request, numero=None):
        ticket = self.get_object()
        conteudo = request.data.get("conteudo")
        if not conteudo:
            return Response({"error": "conteudo é obrigatório"}, status=400)
        # SECURITY: enforce maximum length to prevent DoS / data bloat
        if len(conteudo) > self.RESPOSTA_MAX_LENGTH:
            return Response(
                {
                    "error": f"conteudo excede o limite máximo de {self.RESPOSTA_MAX_LENGTH} caracteres"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        ticket.respostas.create(autor=request.user, conteudo=conteudo)
        return Response({"status": "resposta adicionada"})


class FaturaViewSet(viewsets.ReadOnlyModelViewSet):
    """Client invoices."""

    serializer_class = FaturaSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "numero"
    pagination_class = None

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
        ip = self.request.META.get("REMOTE_ADDR")
        serializer.save(ip_address=ip)


class NotificacaoListView(generics.ListAPIView):
    """User notifications."""

    serializer_class = NotificacaoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return Notificacao.objects.filter(usuario=self.request.user)


class NotificacaoMarcarLidaView(APIView):
    """Mark notification as read."""

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        notificacao = get_object_or_404(Notificacao, pk=pk, usuario=request.user)
        notificacao.lida = True
        notificacao.save()
        return Response({"status": "marcada como lida"})


def health_check(request):
    """Simple health check endpoint — returns 200 OK with JSON status."""
    return JsonResponse({"status": "ok"})
