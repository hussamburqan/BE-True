from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from enrollments.permissions import CanUpdateStatus, IsAdminOrReadOnly

from .models import Enrollment, Participant
from .serializers import (
    EnrollmentCreateSerializer,
    EnrollmentStatusSerializer,
    EnrollmentProgressSerializer,
)
from courses.models import Course


class EnrollmentCreateView(generics.CreateAPIView):
    """
    POST /api/enrollments/  ← تسجيل في دورة
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = EnrollmentCreateSerializer


class UserEnrollmentsView(generics.ListAPIView):
    """
    GET /api/enrollments/user/<participant_id>/
    """
    serializer_class = EnrollmentProgressSerializer

    def get_queryset(self):
        pid = self.kwargs['participant_id']
        return Enrollment.objects.filter(participant_id=pid).select_related('course')


class CourseEnrollmentsView(generics.ListAPIView):
    """
    GET /api/enrollments/course/<course_id>/
    """
    serializer_class = EnrollmentProgressSerializer

    def get_queryset(self):
        cid = self.kwargs['course_id']
        return Enrollment.objects.filter(course_id=cid).select_related('course', 'participant')


class EnrollmentStatusUpdateView(generics.UpdateAPIView):
    """
    PUT /api/enrollments/<id>/status/
    يسمح فقط للمشرف.
    """
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentStatusSerializer
    permission_classes = [CanUpdateStatus]
    lookup_url_kwarg = 'enrollment_id'


class EnrollmentProgressView(generics.RetrieveAPIView):
    """
    GET /api/enrollments/<id>/progress/
    """
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentProgressSerializer
    permission_classes = [permissions.AllowAny]
    lookup_url_kwarg = 'enrollment_id'
