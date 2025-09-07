from rest_framework import generics, viewsets, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from audit.mixins import AuditCreateOnlyMixin
from true.permissions import IsStaffOrSuperuser
from .models import TalentApplication, InternshipApplication
from .serializers import (
    TalentApplicationCreateSerializer,
    TalentAppListSerializer,
    TalentAppDetailSerializer,
    InternshipCreateSerializer,
    InternshipListSerializer,
    InternshipDetailSerializer
)


class PublicJoinTeamView(AuditCreateOnlyMixin, generics.GenericAPIView):
    """
    POST /careers/public/join-team/
    إنشاء طلب انضمام (موظفين/مواهب).
    """
    permission_classes   = [permissions.AllowAny]
    parser_classes       = [MultiPartParser, FormParser]
    serializer_class     = TalentApplicationCreateSerializer

    audit_public_creates = True
    audit_fields         = ["id", "full_name", "email", "status", "created_at", "answers"]

    def post(self, request, *args, **kwargs):
        s = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        out = s.save()

        try:
            app_id = out.get('application_id')
            if app_id:
                instance = TalentApplication.objects.get(pk=app_id)
                self._log_create(instance)
        except Exception:
            pass

        return Response(out, status=status.HTTP_201_CREATED)


class PublicInternshipApplyView(AuditCreateOnlyMixin, generics.GenericAPIView):
    """
    POST /careers/public/internship-apply/
    إنشاء طلب تدريب ميداني لطلبة الجامعات.
    """
    permission_classes   = [permissions.AllowAny]
    parser_classes       = [MultiPartParser, FormParser]
    serializer_class     = InternshipCreateSerializer

    audit_public_creates = True
    audit_fields         = ["id", "full_name", "email", "status", "created_at", "answers"]

    def post(self, request, *args, **kwargs):
        s = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        out = s.save()
        try:
            app_id = out.get('application_id')
            if app_id:
                instance = InternshipApplication.objects.get(pk=app_id)
                self._log_create(instance)
        except Exception:
            pass

        return Response(out, status=status.HTTP_201_CREATED)


class AdminTalentApplicationViewSet(AuditCreateOnlyMixin, viewsets.ModelViewSet):
    """
    CRUD للإدمن على طلبات الانضمام (المواهب).
    - مع فلترة/بحث/ترتيب.
    """
    queryset           = TalentApplication.objects.all()
    permission_classes = [IsStaffOrSuperuser]
    parser_classes     = [MultiPartParser, FormParser]

    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields   = ['status', 'email', 'created_at']
    search_fields      = ['full_name', 'email', 'phone', 'portfolio_url']
    ordering_fields    = ['created_at', 'status', 'full_name']
    ordering           = ['-created_at']

    audit_fields = ["id", "full_name", "email", "status", "created_at"]

    def get_serializer_class(self):
        if self.action == 'list':
            return TalentAppListSerializer
        return TalentAppDetailSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        self._log_create(instance)


class AdminInternshipApplicationViewSet(AuditCreateOnlyMixin, viewsets.ModelViewSet):
    """
    CRUD للإدمن على طلبات التدريب الميداني.
    - مع فلترة/بحث/ترتيب وتمييز واضح عن طلبات الانضمام.
    """
    queryset           = InternshipApplication.objects.all()
    permission_classes = [IsStaffOrSuperuser]
    parser_classes     = [MultiPartParser, FormParser]

    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields   = ['status', 'email', 'university', 'track', 'duration', 'created_at']
    search_fields      = ['full_name', 'email', 'phone', 'university', 'major', 'study_level', 'portfolio_url']
    ordering_fields    = ['created_at', 'status', 'full_name', 'university']
    ordering           = ['-created_at']

    audit_fields = ["id", "full_name", "email", "status", "university", "track", "created_at"]

    def get_serializer_class(self):
        if self.action == 'list':
            return InternshipListSerializer
        return InternshipDetailSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        self._log_create(instance)
