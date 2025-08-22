from django.urls import path
from .views import (
    DashboardView,
    CourseAnalyticsView,
    RevenueAnalyticsView,
    UsersAnalyticsView,
)

urlpatterns = [
    path('analytics/dashboard', DashboardView.as_view(), name='analytics-dashboard'),
    path('analytics/courses',   CourseAnalyticsView.as_view(),   name='analytics-courses'),
    path('analytics/revenue',   RevenueAnalyticsView.as_view(),  name='analytics-revenue'),
    path('analytics/users',     UsersAnalyticsView.as_view(),    name='analytics-users'),
]
