from rest_framework import serializers
from .models import TalentApplication, InternshipApplication
import json


class JSONAnswersMixin:
    def _normalize_answers(self, attrs):
        ans = attrs.get('answers', None)
        if isinstance(ans, str):
            try:
                attrs['answers'] = json.loads(ans or "{}")
            except json.JSONDecodeError:
                raise serializers.ValidationError({'answers': 'invalid_json'})
        if ans is None:
            attrs['answers'] = {}
        return attrs


class TalentApplicationCreateSerializer(JSONAnswersMixin, serializers.ModelSerializer):
    """Public create serializer for Talent applications."""
    answers = serializers.JSONField(required=False, allow_null=True)

    class Meta:
        model  = TalentApplication
        fields = [
            'id', 'full_name', 'email', 'phone',
            'cover_letter', 'portfolio_url', 'cv_file',
            'consent', 'answers', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'status', 'created_at']

    def validate(self, attrs):
        if not attrs.get('consent'):
            raise serializers.ValidationError({'consent': 'required'})
        return self._normalize_answers(attrs)

    def create(self, validated_data):
        app = TalentApplication.objects.create(**validated_data)
        return {'application_id': app.id, 'status': app.status}


class TalentAppListSerializer(serializers.ModelSerializer):
    class Meta:
        model  = TalentApplication
        fields = ['id', 'full_name', 'email', 'phone', 'portfolio_url', 'status', 'created_at']


class TalentAppDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model  = TalentApplication
        fields = [
            'id','full_name','email','phone','cover_letter',
            'portfolio_url','cv_file','consent','answers',
            'status','created_at'
        ]


class InternshipCreateSerializer(JSONAnswersMixin, serializers.ModelSerializer):
    """Public create serializer for Internship applications."""
    answers = serializers.JSONField(required=False, allow_null=True)

    class Meta:
        model  = InternshipApplication
        fields = [
            'id', 'full_name', 'email', 'phone',
            'university', 'major', 'study_level',
            'duration', 'track',
            'experience_text', 'goal', 'strengths', 'teamwork', 'challenge',
            'portfolio_url', 'cv_file',
            'consent', 'answers', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'status', 'created_at']

    def validate(self, attrs):
        if not attrs.get('consent'):
            raise serializers.ValidationError({'consent': 'required'})
        return self._normalize_answers(attrs)

    def create(self, validated_data):
        app = InternshipApplication.objects.create(**validated_data)
        return {'application_id': app.id, 'status': app.status}


class InternshipListSerializer(serializers.ModelSerializer):
    class Meta:
        model  = InternshipApplication
        fields = [
            'id', 'full_name', 'email', 'phone', 'university',
            'track', 'status', 'created_at'
        ]


class InternshipDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model  = InternshipApplication
        fields = [
            'id', 'full_name', 'email', 'phone',
            'university', 'major', 'study_level',
            'duration', 'track',
            'experience_text', 'goal', 'strengths', 'teamwork', 'challenge',
            'portfolio_url', 'cv_file',
            'consent', 'answers', 'status', 'created_at'
        ]
