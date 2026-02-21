"""Serializers for analytics app."""
from rest_framework import serializers


class DashboardSerializer(serializers.Serializer):
    """Dashboard statistics."""
    total_orders = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_customers = serializers.IntegerField()
    total_products = serializers.IntegerField()
    orders_by_status = serializers.DictField()
    recent_orders = serializers.ListField()
    revenue_last_30_days = serializers.DecimalField(max_digits=12, decimal_places=2)
