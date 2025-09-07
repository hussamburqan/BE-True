from django.db import models, transaction
from django.core.validators import RegexValidator, MinValueValidator
from django.core.exceptions import ValidationError
from courses.models import Course

phone_validator = RegexValidator(regex=r'^\+?\d{7,15}$', message='Invalid phone format.')

class Participant(models.Model):
    full_name  = models.CharField(max_length=120, blank=True, default='')
    email      = models.EmailField(unique=True)
    phone      = models.CharField(max_length=20, validators=[phone_validator])
    notes      = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['email']), models.Index(fields=['phone'])]
        ordering = ['-created_at']

    def __str__(self):
        return self.email

class Enrollment(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='enrollments')
    course      = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    created_at  = models.DateTimeField(auto_now_add=True)
    is_active   = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['participant','course'], name='uniq_participant_course')
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.participant.email} -> {self.course_id}'

class Payment(models.Model):
    METHOD_BANK='bank'
    METHOD_CASH='cash'
    METHOD_CHOICES=[(METHOD_BANK,'Bank'),(METHOD_CASH,'Cash')]

    STATUS_PENDING='pending'
    STATUS_RECEIVED='received'
    STATUS_VERIFIED='verified'
    STATUS_CANCELLED='cancelled'
    STATUS_CHOICES=[(STATUS_PENDING,'Pending'),(STATUS_RECEIVED,'Received'),(STATUS_VERIFIED,'Verified'),(STATUS_CANCELLED,'Cancelled')]

    enrollment     = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='payments')
    method         = models.CharField(max_length=10, choices=METHOD_CHOICES)
    amount         = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    currency       = models.CharField(max_length=6, default='USD')
    status         = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    bank_reference = models.CharField(max_length=120, blank=True, default='')
    cash_location  = models.CharField(max_length=120, blank=True, default='')
    note           = models.CharField(max_length=240, blank=True, default='')
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['method']),
            models.Index(fields=['status']),
            models.Index(fields=['enrollment']),
        ]

    def clean(self):
        # لازم enrollment موجود عشان نتحقق من نوع الكورس
        if self.enrollment_id and hasattr(self.enrollment, 'course') and self.enrollment.course:
            if getattr(self.enrollment.course, 'is_online', False) and self.method == self.METHOD_CASH:
                raise ValidationError('In-person cash is not allowed for online courses.')

        # مرجع التحويل مطلوب مع bank
        if self.method == self.METHOD_BANK and not self.bank_reference:
            raise ValidationError('bank_reference is required for bank transfers.')

    def save(self, *args, **kwargs):
        # لو ما في amount وحاطين سعر للكورس، خده تلقائياً
        if (self.amount is None or float(self.amount) == 0.0) and self.enrollment_id and hasattr(self.enrollment, 'course'):
            price = getattr(self.enrollment.course, 'price', None)
            if price is not None:
                self.amount = price
        self.full_clean()
        return super().save(*args, **kwargs)
