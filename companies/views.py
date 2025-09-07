from rest_framework import generics, viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser

from audit.mixins import AuditCreateOnlyMixin
from true.permissions import IsStaffOrSuperuser
from .models import Company
from .serializers import CompanySerializer


class PublicCompanyListView(generics.ListAPIView):
    serializer_class = CompanySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        qs = Company.objects.all().order_by('id')
        active = self.request.query_params.get('active')
        if active is None or active.lower() == 'true':
            qs = qs.filter(is_active=True)
        return qs


class PublicCompanyDetailView(generics.RetrieveAPIView):
    queryset = Company.objects.filter(is_active=True)
    serializer_class = CompanySerializer
    permission_classes = [permissions.AllowAny]


class AdminCompanyViewSet(AuditCreateOnlyMixin, viewsets.ModelViewSet):
    """
    /admin/companies , /admin/companies/<id>
    - يسجّل عمليات الإضافة فقط (create)
    - صلاحيات: ستاف/سوبر فقط
    """
    queryset = Company.objects.all().order_by('id')
    serializer_class = CompanySerializer
    permission_classes = [IsStaffOrSuperuser]
    parser_classes = [MultiPartParser, FormParser]

    audit_fields = ["id", "name", "is_active", "created_at"]
