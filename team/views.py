from rest_framework import viewsets, generics, permissions, filters
from rest_framework.parsers import MultiPartParser, FormParser

from audit.mixins import AuditCreateOnlyMixin
from true.permissions import IsStaffOrSuperuser
from .models import TeamMember
from .serializers import TeamPublicSerializer, TeamAdminSerializer


class PublicTeamListView(generics.ListAPIView):
    """
    GET /public/  => قائمة أعضاء الفريق المفعّلين فقط (بدون pagination)
    """
    queryset = TeamMember.objects.filter(is_active=True).order_by("name", "id")
    serializer_class = TeamPublicSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

class AdminTeamViewSet(AuditCreateOnlyMixin, viewsets.ModelViewSet):
    """
    /admin/teams, /admin/teams/<id>
    CRUD كامل للإدارة عبر الراوتر
    - يسجّل عمليات الإضافة فقط (create) عبر AuditCreateOnlyMixin
    """
    queryset = TeamMember.objects.all().order_by("name", "id")
    serializer_class = TeamAdminSerializer
    permission_classes = [IsStaffOrSuperuser]
    parser_classes = [MultiPartParser, FormParser]

    audit_fields = ["id", "name", "role", "is_active"]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "role"]
    ordering_fields = ["name", "id"]
