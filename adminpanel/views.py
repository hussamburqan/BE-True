from decimal import Decimal

from django.db.models import Count, Sum, Q
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from courses.models   import Course
from payments.models  import Payment
from .models          import SystemLog
from .serializers     import (
    AdminStatsSerializer,
    AdminUserSerializer,
    UserStatusSerializer,
    SystemLogSerializer,
)


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class AdminStatsView(generics.GenericAPIView):
    permission_classes = [AdminOnly]

    def get(self, request):
        User = get_user_model()
        total_users    = User.objects.count()
        active_users   = User.objects.filter(is_active=True).count()
        inactive_users = total_users - active_users

        total_revenue = Payment.objects.filter(status='succeeded').aggregate(
            s=Sum('amount'))['s'] or Decimal('0.00')

        data = AdminStatsSerializer({
            'total_users':   total_users,
            'active_users':  active_users,
            'inactive_users': inactive_users,
            'total_revenue': total_revenue,
            'total_courses': Course.objects.count(),
        }).data
        return Response(data)

class AdminUserListView(generics.ListAPIView):
    """
    يدعم ?search=<query> للبحث بالاسم أو البريد.
    """
    permission_classes = [AdminOnly]
    serializer_class   = AdminUserSerializer
    queryset           = get_user_model().objects.all()
    filter_backends    = [filters.SearchFilter]
    search_fields      = ['name', 'email', 'tel_number']

class UserStatusUpdateView(generics.UpdateAPIView):
    permission_classes = [AdminOnly]
    serializer_class   = UserStatusSerializer
    queryset           = get_user_model().objects.all()
    lookup_url_kwarg   = 'user_id'

    def perform_update(self, serializer):
        instance = serializer.save()
        SystemLog.objects.create(
            level='info',
            message=f"User {instance.id} status changed to {instance.is_active}",
            actor=self.request.user,
        )

class LogPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100


class SystemLogListView(generics.ListAPIView):
    permission_classes = [AdminOnly]
    serializer_class   = SystemLogSerializer
    pagination_class   = LogPagination
    queryset           = SystemLog.objects.all().order_by('-created_at')
    filter_backends    = [filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ['message', 'actor__name', 'level']
    ordering_fields    = ['created_at', 'level']
