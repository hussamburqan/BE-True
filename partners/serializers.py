# app/serializers.py
from rest_framework import serializers
from .models import Partner

class PartnerSerializer(serializers.ModelSerializer):
    # logo: قابل للكتابة/الرفع
    # logo_url: للقراءة فقط (ترجع رابط مطلق)
    logo_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Partner
        fields = [
            "id",
            "name_ar", "name_en",
            "description_ar", "description_en",
            "logo",
            "logo_url",
            "website",
            "is_active",
            "created_at",
        ]

    def get_logo_url(self, obj):
        if not obj.logo:
            return None
        request = self.context.get("request")
        return request.build_absolute_uri(obj.logo.url) if request else obj.logo.url
