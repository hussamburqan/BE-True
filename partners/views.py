from rest_framework import viewsets, generics, permissions, filters
from rest_framework.parsers import MultiPartParser, FormParser

from audit.mixins import AuditCreateOnlyMixin
from true.permissions import IsStaffOrSuperuser
from .models import Partner
from .serializers import PartnerSerializer


class PublicPartnerListView(generics.ListAPIView):
    queryset = Partner.objects.all().order_by('id')
    serializer_class = PartnerSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class AdminPartnerViewSet(AuditCreateOnlyMixin, viewsets.ModelViewSet):
    """
    /admin/partners , /admin/partners/<id>
    - يسجّل عمليات الإضافة فقط (create)
    - صلاحيات: ستاف/سوبر فقط
    """
    queryset = Partner.objects.all().order_by('id')
    serializer_class = PartnerSerializer
    permission_classes = [IsStaffOrSuperuser]
    parser_classes = [MultiPartParser, FormParser]

    audit_fields = ["id"]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']
