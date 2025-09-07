from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PublicEnrollmentCreateView, AdminParticipantViewSet, AdminEnrollmentViewSet, AdminPaymentViewSet

router = DefaultRouter()
router.register(r'admin/participants', AdminParticipantViewSet, basename='admin-participants')
router.register(r'admin/enrollments',  AdminEnrollmentViewSet,  basename='admin-enrollments')
router.register(r'admin/payments',     AdminPaymentViewSet,     basename='admin-payments')

urlpatterns = [
    path('public/', PublicEnrollmentCreateView.as_view(), name='public-enroll'),
    path('', include(router.urls)),
]
