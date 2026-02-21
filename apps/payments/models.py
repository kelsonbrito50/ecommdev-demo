"""Payment model with MercadoPago integration support."""
from django.conf import settings
from django.db import models


class Payment(models.Model):
    """Payment record linked to an order."""

    class Method(models.TextChoices):
        CREDIT_CARD = 'credit_card', 'Credit Card'
        DEBIT_CARD = 'debit_card', 'Debit Card'
        PIX = 'pix', 'PIX'
        BOLETO = 'boleto', 'Boleto'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        CANCELLED = 'cancelled', 'Cancelled'
        REFUNDED = 'refunded', 'Refunded'
        IN_PROCESS = 'in_process', 'In Process'

    order = models.ForeignKey('orders.Order', on_delete=models.PROTECT, related_name='payments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='payments')
    method = models.CharField(max_length=20, choices=Method.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    # MercadoPago fields
    mp_payment_id = models.CharField(max_length=100, blank=True, help_text='MercadoPago payment ID')
    mp_preference_id = models.CharField(max_length=100, blank=True, help_text='MercadoPago preference ID')
    mp_status = models.CharField(max_length=50, blank=True)
    mp_status_detail = models.CharField(max_length=100, blank=True)

    # PIX specific
    pix_qr_code = models.TextField(blank=True)
    pix_qr_code_base64 = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Payment {self.pk} - {self.order.order_number} - {self.status}'
