import base64
from rest_framework import serializers
from django.core.files.base import ContentFile
from .models import TeamMember


class TeamPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model  = TeamMember
        fields = [
            "id", "name", "title", "photo",
            "facebook", "twitter", "instagram", "linkedin", "website",
        ]

class TeamAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model  = TeamMember
        fields = [
            "id", "name", "title",  "photo",
            "facebook", "twitter", "instagram", "linkedin", "website",
            "is_active", "created_at", "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
