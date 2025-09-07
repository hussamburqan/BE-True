from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PublicServiceListView,
    ServiceLatestView,
    AdminServiceViewSet,
)

router = DefaultRouter()
router.register(r'admin/services', AdminServiceViewSet, basename='admin-services')

urlpatterns = [
    path('public/', PublicServiceListView.as_view(), name='public-services-list'),
    path('public/latest/', ServiceLatestView.as_view(), name='public-services-latest'),
    path('', include(router.urls)),
]
