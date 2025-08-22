from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import SystemLog

User = get_user_model()


# ----------  Stats ----------
class AdminStatsSerializer(serializers.Serializer):
    total_users     = serializers.IntegerField()
    active_users    = serializers.IntegerField()
    inactive_users  = serializers.IntegerField()
    total_revenue   = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_courses   = serializers.IntegerField()


# ----------  Users ----------
class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ['id', 'name', 'email', 'tel_number', 'is_active', 'is_staff', 'date_joined']


class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ['is_active']


# ----------  Logs ----------
class SystemLogSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField()

    class Meta:
        model  = SystemLog
        fields = ['id', 'level', 'message', 'actor', 'created_at']
