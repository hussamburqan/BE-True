from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuditLogViewSet

router = DefaultRouter()
router.register(r'admin/audit-logs', AuditLogViewSet, basename='admin-auditlogs')

urlpatterns = [
    path('', include(router.urls)),
]
