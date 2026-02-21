"""Serializers for orders app."""
from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity', 'subtotal']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    item_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total', 'item_count', 'updated_at']


class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_sku', 'price', 'quantity', 'subtotal']
        read_only_fields = ['product_name', 'product_sku', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'status', 'subtotal', 'shipping_cost', 'total',
            'shipping_street', 'shipping_number', 'shipping_complement',
            'shipping_neighborhood', 'shipping_city', 'shipping_state', 'shipping_zipcode',
            'notes', 'items', 'created_at', 'updated_at',
        ]
        read_only_fields = ['order_number', 'subtotal', 'total', 'status']


class CreateOrderSerializer(serializers.ModelSerializer):
    """Create an order from the user's cart."""

    class Meta:
        model = Order
        fields = [
            'shipping_street', 'shipping_number', 'shipping_complement',
            'shipping_neighborhood', 'shipping_city', 'shipping_state',
            'shipping_zipcode', 'notes',
        ]
