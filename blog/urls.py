from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PostPublicListView,
    PostPublicDetailView,
    AdminPostViewSet,
)

router = DefaultRouter()
router.register(r'admin/posts', AdminPostViewSet, basename='admin-posts')

urlpatterns = [
    path('public/', PostPublicListView.as_view(), name='public-posts-list'),
    path('public/<int:pk>/', PostPublicDetailView.as_view(), name='public-posts-detail'),
    path('', include(router.urls)),
]
