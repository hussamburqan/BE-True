from rest_framework import generics, viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from audit.mixins import AuditCreateOnlyMixin
from .models import Course
from .serializers import CourseListSerializer, CourseDetailSerializer
from .filters import CourseFilter
from true.permissions import IsStaffOrSuperuser


class PublicCourseListView(generics.ListAPIView):
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CourseFilter
    search_fields = [
        'title_ar','title_en','description_ar','description_en',
        'instructor_name_ar','instructor_name_en',
    ]
    ordering_fields = ['created_at','price','start_date','registration_end_date']
    ordering = ['-created_at']


class PublicCourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseDetailSerializer
    lookup_field = 'pk'


class AdminCourseViewSet(AuditCreateOnlyMixin, viewsets.ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [IsStaffOrSuperuser]
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CourseFilter
    search_fields = [
        'title_ar','title_en','description_ar','description_en',
        'instructor_name_ar','instructor_name_en',
    ]
    ordering_fields = ['created_at','price','start_date','registration_end_date']
    ordering = ['-created_at']

    audit_fields = ["id", "title_ar", "title_en", "price", "start_date", "registration_end_date", "created_at", "is_active"]

    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        return CourseDetailSerializer
