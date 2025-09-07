from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobListView, JobDetailView, PublicApplyView, AdminJobViewSet, AdminApplicationViewSet

router = DefaultRouter()
router.register(r'admin/jobs', AdminJobViewSet, basename='admin-jobs')
router.register(r'admin/applications', AdminApplicationViewSet, basename='admin-applications')

urlpatterns = [
    path('public/', JobListView.as_view(), name='public-job-list'),
    path('public/<int:pk>/', JobDetailView.as_view(), name='public-job-detail'),
    path('public/apply/', PublicApplyView.as_view(), name='public-job-apply'),

    path('', include(router.urls)),
]
