from rest_framework import viewsets, generics, permissions, filters
from audit.mixins import AuditCreateOnlyMixin
from true.permissions import IsStaffOrSuperuser
from .models import Service
from .serializers import ServiceSerializer

class PublicServiceListView(generics.ListAPIView):
    queryset = Service.objects.all().order_by('-created_at', '-id')
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None  


class ServiceLatestView(generics.ListAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        return Service.objects.order_by("-created_at")[:6]


class AdminServiceViewSet(AuditCreateOnlyMixin, viewsets.ModelViewSet):
    """
    CRUD للأدمن عبر الراوتر:
      /admin/services , /admin/services/<id>
    - يسجّل عمليات الإضافة فقط (create) عبر AuditCreateOnlyMixin
    - صلاحيات: ستاف أو سوبر فقط
    """
    queryset = Service.objects.all().order_by('-created_at', '-id')
    serializer_class = ServiceSerializer
    permission_classes = [IsStaffOrSuperuser]

    audit_fields = ["id", "created_at"] 

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["id"] 
    ordering_fields = ["created_at", "id"]
