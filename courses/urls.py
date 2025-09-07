from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PublicCourseListView,
    PublicCourseDetailByIDView,
    PublicCourseDetailBySlugView,
    AdminCourseViewSet,
)

router = DefaultRouter()
router.register(r'admin/courses', AdminCourseViewSet, basename='admin-courses')

urlpatterns = [
    # عام (لستة)
    path('public/', PublicCourseListView.as_view(), name='public-course-list'),

    path('public/<int:pk>/', PublicCourseDetailByIDView.as_view(), name='public-course-detail'),
    path('public/slug/<slug:slug>/', PublicCourseDetailBySlugView.as_view(), name='public-course-detail-slug'),

    # (اختياري) ألياسات توافق النص التسويقي "training-courses"
    path('public/training-courses/', PublicCourseListView.as_view(), name='public-course-list-alias'),
    path('public/training-courses/<int:pk>/', PublicCourseDetailByIDView.as_view(), name='public-course-detail-alias'),

    # أدمن عبر الراوتر
    path('', include(router.urls)),
]
