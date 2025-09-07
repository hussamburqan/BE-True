from rest_framework import serializers
from .models import PortfolioItem


class PortfolioItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioItem
        fields = ['id', 'title_en', 'title_ar', 'image_cover', 'link']

