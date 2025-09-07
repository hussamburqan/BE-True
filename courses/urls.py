from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PublicCourseListView,
    PublicCourseDetailView,
    AdminCourseViewSet,
)

router = DefaultRouter()
router.register(r'admin/courses', AdminCourseViewSet, basename='admin-courses')

urlpatterns = [
    path('public/', PublicCourseListView.as_view(), name='public-course-list'),
    path('public/<int:pk>/', PublicCourseDetailView.as_view(), name='public-course-detail'),
    path('', include(router.urls)),
]
