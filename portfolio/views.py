from rest_framework import viewsets, generics, permissions, filters
from rest_framework.parsers import MultiPartParser, FormParser

from audit.mixins import AuditCreateOnlyMixin
from true.permissions import IsStaffOrSuperuser
from .models import PortfolioItem
from .serializers import PortfolioItemListSerializer


class PublicPortfolioListView(generics.ListAPIView):
    queryset = PortfolioItem.objects.all()
    serializer_class = PortfolioItemListSerializer
    permission_classes = [permissions.AllowAny]


class PortfolioItemLatestView(generics.ListAPIView):
    serializer_class = PortfolioItemListSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        return PortfolioItem.objects.order_by("-created_at")[:6]


class AdminPortfolioViewSet(AuditCreateOnlyMixin, viewsets.ModelViewSet):
    """
    /admin/portfolio , /admin/portfolio/<id>
    - يسجّل عمليات الإضافة فقط (create)
    - صلاحيات: ستاف/سوبر فقط
    """
    queryset = PortfolioItem.objects.all().order_by("-created_at", "-id")
    serializer_class = PortfolioItemListSerializer
    permission_classes = [IsStaffOrSuperuser]
    parser_classes = [MultiPartParser, FormParser]

    audit_fields = ["id", "created_at"]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["id"]
    ordering_fields = ["created_at", "id"]
