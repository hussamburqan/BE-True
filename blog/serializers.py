import base64
from rest_framework import serializers
from django.core.files.base import ContentFile
from .models import Post

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            fmt, imgstr = data.split(';base64,')
            ext = fmt.split('/')[-1]
            file_data = base64.b64decode(imgstr)
            file_name = f"cover.{ext}"
            return ContentFile(file_data, name=file_name)
        return super().to_internal_value(data)

class PostListSerializer(serializers.ModelSerializer):
    cover_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'slug',
            'title_ar', 'title_en',
            'cover_url', 'created_at'
        ]

    def get_cover_url(self, obj):
        req = self.context.get('request')
        if obj.cover:
            return req.build_absolute_uri(obj.cover.url) if req else obj.cover.url
        return None

class PostDetailSerializer(serializers.ModelSerializer):
    cover_url = serializers.SerializerMethodField()

    class Meta:
        model  = Post
        fields = [
            'id', 'slug',
            'title_ar', 'title_en',
            'content_ar', 'content_en',
            'cover_url', 'created_at', 'updated_at'
        ]

    def get_cover_url(self, obj):
        req = self.context.get('request')
        if obj.cover:
            return req.build_absolute_uri(obj.cover.url) if req else obj.cover.url
        return None

class PostWriteSerializer(serializers.ModelSerializer):
    cover = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model  = Post
        fields = [
            'id', 'slug',
            'title_ar', 'title_en',
            'content_ar', 'content_en',
            'cover', 'is_published'
        ]
        read_only_fields = ['slug']
