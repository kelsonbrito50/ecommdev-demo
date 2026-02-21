"""Views for payments app."""
from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Payment
from .serializers import PaymentSerializer, CreatePaymentSerializer


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """List and retrieve payments for the authenticated user."""
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).select_related('order')


class CreatePaymentView(generics.CreateAPIView):
    """Initiate a new payment (MercadoPago placeholder)."""
    serializer_class = CreatePaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        order = serializer.validated_data['order']
        serializer.save(
            user=self.request.user,
            amount=order.total,
        )
        # TODO: Integrate with MercadoPago SDK here
        # sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
        # preference_data = { ... }
        # result = sdk.preference().create(preference_data)


class WebhookView(APIView):
    """MercadoPago webhook endpoint (placeholder)."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # TODO: Validate MercadoPago signature and process notification
        payment_id = request.data.get('data', {}).get('id')
        if payment_id:
            # Process payment notification
            pass
        return Response({'status': 'ok'})
