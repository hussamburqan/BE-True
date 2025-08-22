import base64
from rest_framework import serializers
from .models import Post, Category
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
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = ['id', 'name', 'slug']

class PostSerializer(serializers.ModelSerializer):
    cover_image = Base64ImageField(required=False, allow_null=True)
    class Meta:
        model  = Post
        fields = ['id','title','slug','category','content','cover_image','created_at']


class PostListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    cover_url = serializers.SerializerMethodField()
    cover_image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model  = Post
        fields = ['id', 'title', 'slug', 'category', 'cover_image', 'created_at']

    def get_cover_url(self, obj):
        req = self.context.get('request')
        return req.build_absolute_uri(obj.cover_image.url) if obj.cover_image else None


class PostDetailSerializer(serializers.ModelSerializer):
    category  = CategorySerializer(read_only=True)
    cover_image = Base64ImageField(required=False, allow_null=True)


    class Meta:
        model  = Post
        fields = [
            'id', 'title', 'slug', 'content',
            'category', 'cover_image',
            'created_at', 'updated_at'
        ]

    def get_cover_url(self, obj):
        req = self.context.get('request')
        return req.build_absolute_uri(obj.cover_image.url) if obj.cover_image else None


class PostAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Post
        fields = [
            'id', 'title', 'content', 'category',
            'cover_image', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
