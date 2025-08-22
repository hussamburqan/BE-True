from django.urls import path
from .views import (
    BookingCreateView,
    BookingListView,
    BookingStatusUpdateView,
    BookingDeleteView,
    AvailabilityView,
)

urlpatterns = [
    path('bookings/', BookingCreateView.as_view(), name='booking-create'),
    path('bookings/availability/', AvailabilityView.as_view(), name='booking-availability'),
    path('bookings/<int:booking_id>/status/', BookingStatusUpdateView.as_view(), name='booking-status'),
    path('bookings/<int:booking_id>/', BookingDeleteView.as_view(), name='booking-delete'),
    path('bookings-admin/', BookingListView.as_view(), name='booking-list'),  # GET كل الحجوزات
]
