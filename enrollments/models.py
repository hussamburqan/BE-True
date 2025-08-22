from django.db import models
from django.utils import timezone
from courses.models import Course   # يفترض أن لديك app اسمه courses

class Participant(models.Model):
    """
    الزائر الذي يسجّل في الدورات.
    """
    name  = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('email', 'phone')  # تجنّب ازدواجية

    def __str__(self):
        return f"{self.name} ({self.email})"


class Enrollment(models.Model):
    """
    ربط Participant مع Course.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    participant = models.ForeignKey(
        Participant, related_name='enrollments', on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course, related_name='enrollments', on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending'
    )
    progress = models.PositiveSmallIntegerField(default=0)  # 0–100 %

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('participant', 'course')

    def __str__(self):
        return f"{self.participant} -> {self.course} ({self.status})"
