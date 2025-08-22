from rest_framework import serializers
from .models import Participant, Enrollment
from courses.serializers import CourseListSerializer  # دورة مختصرة للعرض

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['id', 'name', 'email', 'phone']


class EnrollmentCreateSerializer(serializers.ModelSerializer):
    participant = ParticipantSerializer()

    class Meta:
        model = Enrollment
        fields = ['id', 'participant', 'course']

    def create(self, validated_data):
        participant_data = validated_data.pop('participant')
        participant, _ = Participant.objects.get_or_create(
            email=participant_data['email'],
            phone=participant_data['phone'],
            defaults={'name': participant_data['name']},
        )
        enrollment, _ = Enrollment.objects.get_or_create(
            participant=participant,
            course=validated_data['course'],
        )
        return enrollment


class EnrollmentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['status']


class EnrollmentProgressSerializer(serializers.ModelSerializer):
    course = CourseListSerializer()
    participant = ParticipantSerializer()
    class Meta:
        model = Enrollment
        fields = ['id', 'course','participant', 'progress', 'status']
