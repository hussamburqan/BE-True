from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PublicCompanyListView,
    PublicCompanyDetailView,
    AdminCompanyViewSet,
)

router = DefaultRouter()
router.register(r'admin/companies', AdminCompanyViewSet, basename='admin-companies')

urlpatterns = [
    path('public/', PublicCompanyListView.as_view(), name='public-companies-list'),
    path('public/<int:pk>/', PublicCompanyDetailView.as_view(), name='public-companies-detail'),
    path('', include(router.urls)),
]
