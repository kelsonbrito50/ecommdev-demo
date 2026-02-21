"""Views for orders app."""
from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Cart, CartItem, Order, OrderItem
from .serializers import (
    CartSerializer, CartItemSerializer,
    OrderSerializer, CreateOrderSerializer,
)


class CartView(generics.RetrieveAPIView):
    """Retrieve the authenticated user's cart."""
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart


class CartItemViewSet(viewsets.ModelViewSet):
    """Manage items in the authenticated user's cart."""
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=cart).select_related('product')

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """List and retrieve orders for the authenticated user."""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'order_number'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items')


class CreateOrderView(generics.CreateAPIView):
    """Create a new order from the user's cart."""
    serializer_class = CreateOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        cart = Cart.objects.prefetch_related('items__product').get(user=user)

        if not cart.items.exists():
            raise serializers.ValidationError({'detail': 'Cart is empty.'})

        order = serializer.save(user=user)

        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                product_name=cart_item.product.name,
                product_sku=cart_item.product.sku,
                price=cart_item.product.price,
                quantity=cart_item.quantity,
            )

        order.calculate_totals()
        cart.items.all().delete()
