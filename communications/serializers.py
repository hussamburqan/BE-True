from rest_framework import serializers
from .models import ContactMessage, NewsletterSubscriber


# -------- Contact ----------
class ContactCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ContactMessage
        fields = ['id', 'name', 'email', 'subject', 'message']


class ContactListSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ContactMessage
        fields = ['id', 'name', 'email', 'subject', 'message',
                  'status', 'created_at', 'updated_at']


class ContactStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ContactMessage
        fields = ['status']


# -------- Newsletter ----------
class NewsletterSubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model  = NewsletterSubscriber
        fields = ['id', 'email', 'name']


# -------- Notification send ----------
class NotificationSendSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=255)
    body    = serializers.CharField()
