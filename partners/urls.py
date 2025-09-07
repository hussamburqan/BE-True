from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PublicPartnerListView, AdminPartnerViewSet

router = DefaultRouter()
router.register(r'admin/partners', AdminPartnerViewSet, basename='admin-partners')

urlpatterns = [
    path('public/', PublicPartnerListView.as_view(), name='public-partners-list'),
    path('', include(router.urls)),
]
