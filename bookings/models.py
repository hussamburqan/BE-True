from django.db import models
from django.utils import timezone


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('done', 'Done'),
    ]

    name  = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    scheduled_time = models.DateTimeField()

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('email', 'scheduled_time')  # منع حجزين لنفس الشخص في نفس الوقت
        ordering = ['scheduled_time']

    def __str__(self):
        return f"{self.name} – {self.scheduled_time:%Y-%m-%d %H:%M}"
