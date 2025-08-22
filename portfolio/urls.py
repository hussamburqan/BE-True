from django.urls import path
from .views import (
    PortfolioListView,
    PortfolioDetailView,
    PortfolioCreateView,
    PortfolioUpdateView,
    PortfolioDeleteView,
    PortfoliolatestListView,
)

urlpatterns = [
    # قراءة
    path('',          PortfolioListView.as_view(),   name='portfolio-list'),
    path('portfolio-latest',          PortfoliolatestListView.as_view(),   name='portfolio-list'),
    path('/<int:pk>', PortfolioDetailView.as_view(), name='portfolio-detail'),

    # إدارة (Admin)
    path('',                PortfolioCreateView.as_view(), name='portfolio-create'),
    path('edit-portfolio/<int:item_id>',  PortfolioUpdateView.as_view(), name='portfolio-update'),
    path('/<int:item_id>',  PortfolioDeleteView.as_view(), name='portfolio-delete'),
]
