"""Analytics views - dashboard and stats endpoints."""
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Sum, Count
from django.utils import timezone
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.orders.models import Order
from apps.products.models import Product

User = get_user_model()


class DashboardView(APIView):
    """Admin dashboard with key e-commerce metrics."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        now = timezone.now()
        thirty_days_ago = now - timedelta(days=30)

        total_orders = Order.objects.count()
        total_revenue = Order.objects.filter(
            status__in=['confirmed', 'processing', 'shipped', 'delivered']
        ).aggregate(total=Sum('total'))['total'] or 0

        revenue_30d = Order.objects.filter(
            created_at__gte=thirty_days_ago,
            status__in=['confirmed', 'processing', 'shipped', 'delivered'],
        ).aggregate(total=Sum('total'))['total'] or 0

        orders_by_status = dict(
            Order.objects.values_list('status').annotate(count=Count('id')).order_by('status')
        )

        recent_orders = list(
            Order.objects.order_by('-created_at')[:10].values(
                'order_number', 'status', 'total', 'created_at'
            )
        )

        return Response({
            'total_orders': total_orders,
            'total_revenue': str(total_revenue),
            'total_customers': User.objects.filter(is_staff=False).count(),
            'total_products': Product.objects.filter(is_active=True).count(),
            'orders_by_status': orders_by_status,
            'recent_orders': recent_orders,
            'revenue_last_30_days': str(revenue_30d),
        })


class RevenueByPeriodView(APIView):
    """Revenue breakdown by day for the last N days."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)

        data = (
            Order.objects
            .filter(created_at__gte=start_date, status__in=['confirmed', 'processing', 'shipped', 'delivered'])
            .extra(select={'day': "DATE(created_at)"})
            .values('day')
            .annotate(revenue=Sum('total'), count=Count('id'))
            .order_by('day')
        )

        return Response(list(data))
