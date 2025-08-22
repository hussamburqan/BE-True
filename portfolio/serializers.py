import base64
from rest_framework import serializers
from .models import PortfolioItem
from django.core.files.base import ContentFile
class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            file_data = base64.b64decode(imgstr)
            file_name = f"temp.{ext}"
            return ContentFile(file_data, name=file_name)
        return super().to_internal_value(data)
class PortfolioSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model  = PortfolioItem
        fields = [
            'id', 'title', 'description',
            'image',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_image_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url) if obj.image else None
