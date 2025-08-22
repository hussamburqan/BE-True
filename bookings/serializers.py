from datetime import timezone
from rest_framework import serializers
from .models import Booking


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'name', 'email', 'phone', 'scheduled_time']

    def validate_scheduled_time(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Choose a future time.")
        return value


class BookingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'id', 'name', 'email', 'phone',
            'scheduled_time', 'status', 'created_at'
        ]


class BookingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['status']
