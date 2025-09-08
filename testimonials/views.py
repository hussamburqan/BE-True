from rest_framework import viewsets, generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser

from audit.mixins import AuditCreateOnlyMixin
from true.permissions import IsStaffOrSuperuser, IsStaffOrSuperuserOrReadOnly
from .models import Testimonial
from .serializers import TestimonialSerializer


class AdminTestimonialViewSet(AuditCreateOnlyMixin, viewsets.ModelViewSet):
    """
    CRUD للإدارة عبر الراوتر: /admin/testimonials ...
    نسجّل فقط عمليات الإضافة (create).
    """
    queryset = Testimonial.objects.all().order_by('-created_at', 'id')
    serializer_class = TestimonialSerializer
    permission_classes = [IsStaffOrSuperuser]
    parser_classes = [MultiPartParser, FormParser]
    audit_fields = ["id", "author_name", "text", "created_at"] 


class PublicTestimonialCreateView(generics.CreateAPIView):
    
    queryset = Testimonial.objects.none()
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]
