from django.urls import path
from .views import (
    EnrollmentCreateView,
    UserEnrollmentsView,
    CourseEnrollmentsView,
    EnrollmentStatusUpdateView,
    EnrollmentProgressView,
)

urlpatterns = [
    path('enrollments', EnrollmentCreateView.as_view(), name='enrollment-create'),
    path('enrollments/user/<int:participant_id>', UserEnrollmentsView.as_view(), name='user-enrollments'),
    path('enrollments/course/<int:course_id>', CourseEnrollmentsView.as_view(), name='course-enrollments'),
    path('enrollments/<int:enrollment_id>/status', EnrollmentStatusUpdateView.as_view(), name='enrollment-status'),
    path('enrollments/<int:enrollment_id>/progress', EnrollmentProgressView.as_view(), name='enrollment-progress'),
]
