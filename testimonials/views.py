from rest_framework import viewsets, generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser

from audit.mixins import AuditCreateOnlyMixin
from true.permissions import IsStaffOrSuperuser
from .models import Testimonial
from .serializers import TestimonialSerializer

class AdminTestimonialViewSet(AuditCreateOnlyMixin, viewsets.ModelViewSet):
    queryset = Testimonial.objects.all().order_by('-created_at', 'id')
    serializer_class = TestimonialSerializer
    permission_classes = [IsStaffOrSuperuser]
    parser_classes = [MultiPartParser, FormParser]
    audit_fields = ["id", "author_name", "text", "created_at"]


class PublicTestimonialView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = TestimonialSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        qs = Testimonial.objects.all().order_by('-created_at', 'id')
        if hasattr(Testimonial, 'is_active'):
            qs = qs.filter(is_active=True)
        return qs
