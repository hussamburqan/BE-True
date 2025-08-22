from django.core.mail import send_mass_mail
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from communications.permissions import CanMessage

from .models import ContactMessage, NewsletterSubscriber
from .serializers import (
    ContactCreateSerializer,
    ContactListSerializer,
    ContactStatusSerializer,
    NewsletterSubscribeSerializer,
    NotificationSendSerializer,
)


# ---------- Contact ----------
class ContactCreateView(generics.CreateAPIView):
    serializer_class = ContactCreateSerializer
    permission_classes = [permissions.AllowAny]


class ContactListView(generics.ListAPIView):
    queryset = ContactMessage.objects.all().order_by('-created_at')
    serializer_class = ContactListSerializer
    permission_classes = [CanMessage]


class ContactStatusUpdateView(generics.UpdateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactStatusSerializer
    permission_classes = [CanMessage]
    lookup_url_kwarg = 'message_id'


# ---------- Newsletter ----------
class NewsletterSubscribeView(generics.CreateAPIView):
    serializer_class = NewsletterSubscribeSerializer
    permission_classes = [CanMessage]


# ---------- Notifications ----------
class NotificationSendView(generics.GenericAPIView):
    """
    يرسل رسالة بريد جماعي لكل المشتركين في النشرة.
    """
    serializer_class = NotificationSendSerializer
    permission_classes = [CanMessage]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        subject = serializer.validated_data['subject']
        body    = serializer.validated_data['body']

        recipients = NewsletterSubscriber.objects.values_list('email', flat=True)
        if not recipients:
            return Response({"detail": "No subscribers."}, status=status.HTTP_400_BAD_REQUEST)

        # تحضير رسائل البريد
        from_email = settings.DEFAULT_FROM_EMAIL
        messages = [(subject, body, from_email, [email]) for email in recipients]

        send_mass_mail(messages, fail_silently=False)
        return Response({"detail": f"Notification sent to {len(messages)} subscribers."})
