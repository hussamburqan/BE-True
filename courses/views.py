from rest_framework import generics, viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from audit.mixins import AuditCreateOnlyMixin
from .models import Course
from .serializers import CourseListSerializer, CourseDetailSerializer
from .filters import CourseFilter
from true.permissions import IsStaffOrSuperuser

# ===== Public =====
class PublicCourseListView(generics.ListAPIView):
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseListSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CourseFilter  # يظل شغّال لو ضفت حقول جديدة في الفلتر

    # بحث أوسع (عناوين/وصف/مكان/مدرب)
    search_fields = [
        'title_ar','title_en','description_ar','description_en',
        'instructor_name_ar','instructor_name_en',
        'location_ar','location_en',
    ]

    # ترتيب يشمل تمييز الكورس
    ordering_fields = ['created_at','price','start_date','registration_end_date','is_featured']
    ordering = ['-is_featured', '-created_at']  # المميّز أولاً ثم الأحدث


class PublicCourseDetailByIDView(generics.RetrieveAPIView):
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseDetailSerializer
    lookup_field = 'pk'


class PublicCourseDetailBySlugView(generics.RetrieveAPIView):
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseDetailSerializer
    lookup_field = 'slug'


# ===== Admin (Router) =====
class AdminCourseViewSet(AuditCreateOnlyMixin, viewsets.ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [IsStaffOrSuperuser]
    parser_classes = [MultiPartParser, FormParser]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CourseFilter

    search_fields = [
        'title_ar','title_en','description_ar','description_en',
        'instructor_name_ar','instructor_name_en',
        'location_ar','location_en','slug',
    ]
    ordering_fields = ['created_at','price','start_date','registration_end_date','is_featured']
    ordering = ['-created_at']

    # الحقول اللي بتتسجل في لوحة التدقيق عند الإنشاء
    audit_fields = [
        "id", "slug", "title_ar", "title_en",
        "price", "currency", "attendance_mode",
        "start_date", "registration_end_date",
        "is_active", "is_featured", "created_at",
    ]

    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        return CourseDetailSerializer
