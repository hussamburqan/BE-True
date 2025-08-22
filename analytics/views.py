import calendar
from datetime import datetime, timedelta

from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from rest_framework import permissions, generics, status
from rest_framework.response import Response

from authentiocation.models        import User          # نموذج المستخدم المخصّص
from courses.models      import Course
from enrollments.models  import Enrollment
from payments.models     import Payment

from .serializers import (
    DashboardSerializer,
    CourseStatSerializer,
    RevenueStatSerializer,
    UsersStatSerializer,
)


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


# ----------  لوحة عامة ----------
class DashboardView(generics.GenericAPIView):
    permission_classes = [AdminOnly]

    def get(self, request):
        data = {
            "total_users":      User.objects.count(),
            "total_courses":    Course.objects.count(),
            "total_revenue":    Payment.objects.filter(status='succeeded').aggregate(
                                    s=Sum('amount'))['s'] or 0,
            "total_enrollments": Enrollment.objects.count(),
        }
        return Response(DashboardSerializer(data).data)


# ----------  إحصاءات الدورات ----------
class CourseAnalyticsView(generics.GenericAPIView):
    permission_classes = [AdminOnly]

    def get(self, request):
        qs = (Course.objects
              .annotate(enrollments=Count('enrollments'))
              .order_by('-enrollments')[:10])

        data = [
            CourseStatSerializer({
                "course_id": c.id,
                "course_title": c.title,
                "enrollments": c.enrollments,
            }).data
            for c in qs
        ]
        return Response(data)


# ----------  إحصاءات الإيرادات ----------
class RevenueAnalyticsView(generics.GenericAPIView):
    permission_classes = [AdminOnly]

    def get(self, request):
        six_months_ago = datetime.now() - timedelta(days=180)
        qs = (
            Payment.objects
            .filter(created_at__gte=six_months_ago, status='succeeded')
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(revenue=Sum('amount'))
            .order_by('month')
        )

        data = [
            RevenueStatSerializer({
                "month": f"{row['month'].year}-{row['month'].month:02}",
                "revenue": row['revenue'],
            }).data
            for row in qs
        ]
        return Response(data)


# ----------  إحصاءات المستخدمين ----------
class UsersAnalyticsView(generics.GenericAPIView):
    permission_classes = [AdminOnly]

    def get(self, request):
        six_months_ago = datetime.now() - timedelta(days=180)
        qs = (
            User.objects
            .filter(date_joined__gte=six_months_ago)
            .annotate(month=TruncMonth('date_joined'))
            .values('month')
            .annotate(users=Count('id'))
            .order_by('month')
        )

        data = [
            UsersStatSerializer({
                "month": f"{row['month'].year}-{row['month'].month:02}",
                "users": row['users'],
            }).data
            for row in qs
        ]
        return Response(data)
