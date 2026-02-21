"""Serializers for payments app."""
from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    order_number = serializers.UUIDField(source='order.order_number', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'order', 'order_number', 'method', 'status', 'amount',
            'mp_payment_id', 'mp_status', 'pix_qr_code', 'pix_qr_code_base64',
            'created_at', 'updated_at',
        ]
        read_only_fields = [
            'status', 'mp_payment_id', 'mp_status',
            'pix_qr_code', 'pix_qr_code_base64',
        ]


class CreatePaymentSerializer(serializers.ModelSerializer):
    """Initiate a payment for an order."""

    class Meta:
        model = Payment
        fields = ['order', 'method']
