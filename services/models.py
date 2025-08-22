from django.db import models
from django.utils import timezone


class Service(models.Model):
    title       = models.CharField(max_length=255)
    description = models.TextField()
    price       = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    service        = models.ForeignKey(Service, related_name='requests', on_delete=models.CASCADE)
    customer_name  = models.CharField(max_length=255)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)

    details        = models.TextField(blank=True)
    status         = models.CharField(max_length=12, choices=STATUS_CHOICES, default='pending')

    created_at     = models.DateTimeField(default=timezone.now)
    updated_at     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer_name} – {self.service}"
