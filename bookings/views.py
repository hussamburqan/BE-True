from datetime import timedelta, time, datetime

from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Booking
from .serializers import (
    BookingCreateSerializer,
    BookingListSerializer,
    BookingStatusSerializer,
)


# -------------  إنشاء حجز  -------------
class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingCreateSerializer
    permission_classes = [permissions.AllowAny]


# -------------  جلب كل الحجوزات (Admin) -------------
class BookingListView(generics.ListAPIView):
    queryset = Booking.objects.all().select_related(None)
    serializer_class = BookingListSerializer
    permission_classes = [permissions.IsAdminUser]


# -------------  تحديث حالة الحجز (Admin) -------------
class BookingStatusUpdateView(generics.UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingStatusSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_url_kwarg = 'booking_id'


# -------------  إلغاء حجز (Admin) -------------
class BookingDeleteView(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    permission_classes = [permissions.IsAdminUser]
    lookup_url_kwarg = 'booking_id'


# -------------  المواعيد المتاحة -------------
class AvailabilityView(generics.GenericAPIView):
    """
    تعيد قائمة ISO‑8601 datetimes المتاحة للأيام السبعة القادمة
    بين 09:00 و 17:00 بفاصل ساعة واحدة، مع استثناء الأوقات المحجوزة.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        now = timezone.localtime()
        start_date = now.date()
        end_date = start_date + timedelta(days=7)

        # أوقات العمل
        work_start = time(hour=9)
        work_end   = time(hour=17)
        slot_len   = timedelta(hours=1)

        # جلب الحجوزات خلال الفترة
        taken = set(
            Booking.objects.filter(
                scheduled_time__date__gte=start_date,
                scheduled_time__date__lte=end_date,
            ).values_list('scheduled_time', flat=True)
        )

        available = []
        day = start_date
        while day <= end_date:
            slot = datetime.combine(day, work_start, tzinfo=now.tzinfo)
            end_of_day = datetime.combine(day, work_end, tzinfo=now.tzinfo)
            while slot <= end_of_day:
                if slot not in taken and slot > now:
                    available.append(slot.isoformat())
                slot += slot_len
            day += timedelta(days=1)

        return Response({"available_slots": available})
