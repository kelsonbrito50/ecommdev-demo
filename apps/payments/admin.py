"""Admin configuration for payments app."""
from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'user', 'method', 'status', 'amount', 'created_at']
    list_filter = ['status', 'method', 'created_at']
    search_fields = ['order__order_number', 'user__email', 'mp_payment_id']
    readonly_fields = ['mp_payment_id', 'mp_preference_id', 'mp_status', 'mp_status_detail']
