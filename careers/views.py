from rest_framework import generics, viewsets, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from audit.mixins import AuditCreateOnlyMixin
from .models import Job, JobApplication
from .serializers import (
    JobListSerializer, JobDetailSerializer,
    PublicApplicationCreateSerializer,
)
from true.permissions import IsStaffOrSuperuser


class JobListView(generics.ListAPIView):
    queryset = Job.objects.filter(is_active=True)
    serializer_class = JobListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['department','employment_type','is_remote']


class JobDetailView(generics.RetrieveAPIView):
    queryset = Job.objects.filter(is_active=True)
    serializer_class = JobDetailSerializer
    lookup_field = 'pk'


class PublicApplyView(AuditCreateOnlyMixin, generics.GenericAPIView):
    """
    تقديم طلب توظيف عام.
    - نسجّل الإضافة فقط (create) حتى لو المستخدم مش مسجّل (audit_public_creates=True).
    """
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.AllowAny]
    serializer_class = PublicApplicationCreateSerializer

    audit_public_creates = True
    audit_fields = ["id", "job_id", "full_name", "email", "status", "created_at"]  

    def post(self, request, *args, **kwargs):
        s = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        out = s.save()

        application = None
        if isinstance(out, JobApplication):
            application = out
        elif hasattr(s, "instance") and isinstance(s.instance, JobApplication):
            application = s.instance
        elif isinstance(out, dict):
            for key in ("application", "application_id", "id"):
                val = out.get(key)
                if val:
                    try:
                        application = JobApplication.objects.get(pk=val)
                        break
                    except JobApplication.DoesNotExist:
                        pass

        if application is not None:
            self._log_create(application)

        return Response(out, status=status.HTTP_201_CREATED)


from rest_framework import serializers

class AdminJobViewSet(AuditCreateOnlyMixin, viewsets.ModelViewSet):
    """
    - يسجّل الإضافة فقط عند إنشاء Job جديد.
    """
    queryset = Job.objects.all()
    permission_classes = [IsStaffOrSuperuser]
    serializer_class = JobDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active','department','employment_type','is_remote']

    audit_fields = ["id", "title_en", "title_ar", "is_active", "created_at"]  # عدّل حسب حقولك


class AdminApplicationViewSet(AuditCreateOnlyMixin, viewsets.ModelViewSet):
    """
    - يسجّل الإضافة فقط عند إنشاء JobApplication جديد.
    """
    queryset = JobApplication.objects.select_related('job').all()
    permission_classes = [IsStaffOrSuperuser]

    class AppSerializer(serializers.ModelSerializer):
        job_title = serializers.SerializerMethodField()
        class Meta:
            model = JobApplication
            fields = ['id','job','job_title','full_name','email','phone','cover_letter',
                      'portfolio_url','cv_file','status','consent','created_at']
        def get_job_title(self, obj):
            return (obj.job.title_en or obj.job.title_ar)

    serializer_class = AppSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status','job']

    audit_fields = ["id", "job_id", "full_name", "email", "status", "created_at"]
