from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PublicPortfolioListView,
    PortfolioItemLatestView,
    AdminPortfolioViewSet,
)

router = DefaultRouter()
router.register(r'admin/portfolio', AdminPortfolioViewSet, basename='admin-portfolio')

urlpatterns = [
    path('public/', PublicPortfolioListView.as_view(), name='public-portfolio-list'),
    path('public/latest/', PortfolioItemLatestView.as_view(), name='public-portfolio-latest'),
    path('', include(router.urls)),
]
