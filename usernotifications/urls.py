from django.urls import path
from .views import (
    NotificationListView,
    NotificationReadView,
    NotificationMarkAllReadView,
)

urlpatterns = [
    path('notifications',                NotificationListView.as_view(),      name='notif-list'),
    path('notifications/<int:notif_id>/read', NotificationReadView.as_view(), name='notif-read'),
    path('notifications/mark-all-read',  NotificationMarkAllReadView.as_view(), name='notif-mark-all'),
]
