from django.urls import path
from .views import (
    ContactCreateView,
    ContactListView,
    ContactStatusUpdateView,
    NewsletterSubscribeView,
    NotificationSendView,
)

urlpatterns = [
    # Contact
    path('contact',              ContactCreateView.as_view(), name='contact-send'),
    path('contact/messages',     ContactListView.as_view(),   name='contact-messages'),
    path('contact/messages/<int:message_id>', ContactStatusUpdateView.as_view(), name='contact-status'),

    # Newsletter
    path('newsletter/subscribe', NewsletterSubscribeView.as_view(), name='newsletter-subscribe'),

    # Notifications
    path('notifications/send',   NotificationSendView.as_view(), name='notifications-send'),
]
            