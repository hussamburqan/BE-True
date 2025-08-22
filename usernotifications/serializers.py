from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Notification
        fields = ['id', 'title', 'body', 'is_read', 'created_at']
        read_only_fields = fields   # للقراءة فقط


class MarkReadSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Notification
        fields = ['is_read']
