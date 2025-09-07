from rest_framework import generics, viewsets, permissions, status, decorators
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from audit.mixins import AuditCreateOnlyMixin
from .serializers import (
    PublicEnrollmentCreateSerializer,
    ParticipantSerializer, EnrollmentSerializer, PaymentSerializer
)
from .models import Participant, Enrollment, Payment
from true.permissions import IsStaffOrSuperuser


class PublicEnrollmentCreateView(AuditCreateOnlyMixin, generics.GenericAPIView):
    """
    يسجّل إنشاء الـ Enrollment (إضافة فقط). بما إنّه public، فعّلنا audit_public_creates.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = PublicEnrollmentCreateSerializer

    audit_public_creates = True

    audit_fields = ["id", "participant_id", "course_id", "status", "created_at"]

    def post(self, request, *args, **kwargs):
        s = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        out = s.save()

        enrollment = None

        if isinstance(out, Enrollment):
            enrollment = out

        elif hasattr(s, "instance") and isinstance(s.instance, Enrollment):
            enrollment = s.instance

        elif isinstance(out, dict):
            possible_keys = ("enrollment", "enrollment_id", "id")
            for k in possible_keys:
                eid = out.get(k)
                if eid:
                    try:
                        enrollment = Enrollment.objects.get(pk=eid)
                        break
                    except Enrollment.DoesNotExist:
                        pass

        if enrollment is not None:
            self._log_create(enrollment)

        return Response(out, status=status.HTTP_201_CREATED)


class AdminParticipantViewSet(AuditCreateOnlyMixin, viewsets.ModelViewSet):
    """
    يسجّل عمليات الإضافة فقط ل Participant.
    """
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [IsStaffOrSuperuser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['email', 'phone']
    search_fields = ['email', 'phone', 'full_name']
    ordering = ['-created_at']

    audit_fields = ["id", "full_name", "email", "phone", "created_at"]


class AdminEnrollmentViewSet(AuditCreateOnlyMixin, viewsets.ModelViewSet):
    """
    يسجّل عمليات الإضافة فقط ل Enrollment.
    """
    queryset = Enrollment.objects.select_related('participant', 'course').all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsStaffOrSuperuser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active', 'course', 'participant']
    search_fields = ['participant__email', 'participant__full_name', 'course__title_en', 'course__title_ar']
    ordering = ['-created_at']

    audit_fields = ["id", "participant_id", "course_id", "is_active", "created_at"]


class AdminPaymentViewSet(AuditCreateOnlyMixin, viewsets.ModelViewSet):
    """
    يسجّل عمليات الإضافة فقط ل Payment.
    الإجراءات السريعة أدناه (verify/cancel/...) هي تحديثات، لن يتم تسجيلها (حسب طلبك).
    """
    queryset = Payment.objects.select_related('enrollment', 'enrollment__participant', 'enrollment__course').all()
    serializer_class = PaymentSerializer
    permission_classes = [IsStaffOrSuperuser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'method', 'enrollment', 'enrollment__course']
    search_fields = ['bank_reference', 'note', 'enrollment__participant__email']
    ordering = ['-created_at']

    audit_fields = ["id", "enrollment_id", "status", "method", "created_at"]

    @decorators.action(detail=True, methods=['post'])
    def mark_received(self, request, pk=None):
        p = self.get_object()
        p.status = Payment.STATUS_RECEIVED
        p.save(update_fields=['status'])
        return Response({'status': p.status})

    @decorators.action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        p = self.get_object()
        p.status = Payment.STATUS_VERIFIED
        p.save(update_fields=['status'])
        return Response({'status': p.status})

    @decorators.action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        p = self.get_object()
        p.status = Payment.STATUS_CANCELLED
        p.save(update_fields=['status'])
        return Response({'status': p.status})
