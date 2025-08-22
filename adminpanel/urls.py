from django.urls import path
from .views import (
    AdminStatsView,
    AdminUserListView,
    UserStatusUpdateView,
    SystemLogListView,
)

urlpatterns = [
    path('admin/stats',            AdminStatsView.as_view(),       name='admin-stats'),
    path('admin/users',            AdminUserListView.as_view(),    name='admin-users'),
    path('admin/users/<int:user_id>/status', UserStatusUpdateView.as_view(), name='admin-user-status'),
    path('admin/system-logs',      SystemLogListView.as_view(),    name='admin-system-logs'),
]
