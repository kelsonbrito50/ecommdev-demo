"""Faturas app views."""
import hashlib
import hmac
import json
import logging
import re

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, TemplateView, View

from .models import Fatura, Pagamento

logger = logging.getLogger(__name__)


class FaturaListView(LoginRequiredMixin, ListView):
    """List all client invoices."""
    model = Fatura
    template_name = 'faturas/lista.html'
    context_object_name = 'faturas'

    def get_queryset(self):
        return Fatura.objects.filter(cliente=self.request.user)


class FaturaDetailView(LoginRequiredMixin, DetailView):
    """Invoice detail page."""
    model = Fatura
    template_name = 'faturas/detalhe.html'
    context_object_name = 'fatura'
    slug_field = 'numero'
    slug_url_kwarg = 'numero'

    def get_queryset(self):
        return Fatura.objects.filter(cliente=self.request.user)


class FaturaPagarView(LoginRequiredMixin, TemplateView):
    """Payment page for invoice."""
    template_name = 'faturas/pagar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fatura'] = get_object_or_404(
            Fatura,
            numero=self.kwargs['numero'],
            cliente=self.request.user
        )
        return context


class FaturaPDFView(LoginRequiredMixin, View):
    """Generate PDF for invoice."""

    def get(self, request, numero):
        fatura = get_object_or_404(
            Fatura,
            numero=numero,
            cliente=request.user
        )
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{fatura.numero}.pdf"'
        return response


@method_decorator(csrf_exempt, name='dispatch')
class MercadoPagoWebhookView(View):
    """
    Mercado Pago payment webhook with signature verification.

    Mercado Pago sends webhooks with an x-signature header containing:
    - ts: timestamp of when the notification was sent
    - v1: HMAC-SHA256 signature

    The signature is computed over: id={data.id};request-id={x-request-id};ts={ts};
    """

    def _parse_signature_header(self, signature_header):
        """
        Parse the x-signature header into components.
        Format: ts=<timestamp>,v1=<hash>
        """
        if not signature_header:
            return None, None

        parts = {}
        for part in signature_header.split(','):
            if '=' in part:
                key, value = part.split('=', 1)
                parts[key.strip()] = value.strip()

        return parts.get('ts'), parts.get('v1')

    def _verify_signature(self, request, data):
        """
        Verify the Mercado Pago webhook signature.

        Returns True if signature is valid, False otherwise.
        """
        webhook_secret = getattr(settings, 'MERCADOPAGO_WEBHOOK_SECRET', None)

        if not webhook_secret:
            logger.error(
                "MERCADOPAGO_WEBHOOK_SECRET not configured. "
                "Blocking webhook request for security."
            )
            return False  # Block - do not process without verification

        signature_header = request.headers.get('x-signature', '')
        request_id = request.headers.get('x-request-id', '')

        ts, received_hash = self._parse_signature_header(signature_header)

        if not ts or not received_hash:
            logger.warning("Missing timestamp or hash in x-signature header")
            return False

        data_id = data.get('data', {}).get('id', '')

        manifest = f"id={data_id};request-id={request_id};ts={ts};"

        computed_hash = hmac.new(
            webhook_secret.encode('utf-8'),
            manifest.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        is_valid = hmac.compare_digest(computed_hash, received_hash)

        if not is_valid:
            logger.warning(
                f"Invalid webhook signature. "
                f"Request ID: {request_id}, Data ID: {data_id}"
            )

        return is_valid

    def post(self, request):
        try:
            data = json.loads(request.body)

            if not self._verify_signature(request, data):
                logger.warning(
                    f"Webhook signature verification failed. "
                    f"IP: {request.META.get('REMOTE_ADDR')}"
                )
                return JsonResponse(
                    {'error': 'Invalid signature'},
                    status=401
                )

            action = data.get('action')
            payment_id = data.get('data', {}).get('id')

            if action == 'payment.created' and payment_id:
                # Security (4.1): Idempotency check — reject duplicate webhooks
                # for the same transaction ID to prevent replay attacks.
                transacao_id = str(payment_id)
                if Pagamento.objects.filter(transacao_id=transacao_id).exists():
                    logger.info(
                        f"Duplicate webhook ignored (already processed): "
                        f"transacao_id={transacao_id}"
                    )
                    return JsonResponse({'status': 'already processed'})

                logger.info(f"Processing payment notification: {payment_id}")
                # TODO: Implement payment processing logic
                # self._process_payment(payment_id)

            return JsonResponse({'status': 'ok'})

        except json.JSONDecodeError:
            logger.error("Invalid JSON in webhook request body")
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.exception(f"Error processing webhook: {e}")
            return JsonResponse({'error': 'Internal error'}, status=500)
