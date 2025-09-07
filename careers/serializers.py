from rest_framework import serializers
from django.utils import timezone
from .models import Job, JobApplication

class JobListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'id','title_ar','title_en','department','location_ar','location_en',
            'employment_type','is_remote','apply_deadline','is_active','created_at'
        ]

class JobDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'id','title_ar','title_en','department','location_ar','location_en',
            'employment_type','is_remote',
            'description_ar','description_en','requirements_ar','requirements_en',
            'salary_min','salary_max','currency','apply_deadline',
            'is_active','created_at','updated_at'
        ]

class PublicApplicationCreateSerializer(serializers.Serializer):
    job = serializers.PrimaryKeyRelatedField(queryset=Job.objects.filter(is_active=True))
    full_name = serializers.CharField(max_length=120)
    email     = serializers.EmailField()
    phone     = serializers.CharField(max_length=20)
    cover_letter = serializers.CharField(allow_blank=True, required=False)
    portfolio_url = serializers.URLField(allow_blank=True, required=False)
    consent   = serializers.BooleanField()
    cv_file   = serializers.FileField(allow_empty_file=False, required=False)

    def validate(self, attrs):
        job: Job = attrs['job']

        if job.apply_deadline:
            from datetime import date, datetime
            if isinstance(job.apply_deadline, datetime):
                closed = job.apply_deadline.date() < timezone.localdate()
            else:
                closed = job.apply_deadline < timezone.localdate()
            if closed:
                raise serializers.ValidationError({'job': 'application_closed'})
        if not attrs.get('consent'):
            raise serializers.ValidationError({'consent': 'required'})
        return attrs

    def create(self, validated):
        app = JobApplication.objects.create(**validated)
        return {'application_id': app.id, 'status': app.status}
