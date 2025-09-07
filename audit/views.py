from rest_framework import viewsets, permissions
from .models import AuditLog
from .serializers import AuditLogSerializer
from true.permissions import IsStaffOrSuperuser

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsStaffOrSuperuser]
