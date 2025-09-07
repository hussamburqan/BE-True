from rest_framework import serializers
from .models import Course

class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id','title_ar','title_en','description_ar','description_en',
            'image','price','start_date','end_date','registration_end_date',
            'instructor_name_ar','instructor_name_en','instructor_photo',
            'is_active','created_at','is_online'
        ]

class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id','title_ar','title_en','description_ar','description_en',
            'curriculum_ar','curriculum_en','image','price',
            'start_date','end_date','registration_end_date',
            'instructor_name_ar','instructor_name_en','instructor_photo',
            'is_active','created_at','updated_at','is_online'
        ]
