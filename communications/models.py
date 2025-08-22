from django.db import models
from django.utils import timezone


class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In progress'),
        ('resolved', 'Resolved'),
    ]

    name    = models.CharField(max_length=255)
    email   = models.EmailField()
    subject = models.CharField(max_length=255, blank=True)
    message = models.TextField()

    status  = models.CharField(max_length=12, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} – {self.subject or 'No subject'}"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    name  = models.CharField(max_length=255, blank=True)
    subscribed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email
