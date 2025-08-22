from rest_framework import serializers


class DashboardSerializer(serializers.Serializer):
    total_users     = serializers.IntegerField()
    total_courses   = serializers.IntegerField()
    total_revenue   = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_enrollments = serializers.IntegerField()


class CourseStatSerializer(serializers.Serializer):
    course_id   = serializers.IntegerField()
    course_title = serializers.CharField()
    enrollments = serializers.IntegerField()


class RevenueStatSerializer(serializers.Serializer):
    month   = serializers.CharField()   # مثلاً 2025‑07
    revenue = serializers.DecimalField(max_digits=12, decimal_places=2)


class UsersStatSerializer(serializers.Serializer):
    month = serializers.CharField()
    users = serializers.IntegerField()
