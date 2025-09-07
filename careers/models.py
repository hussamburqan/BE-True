from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

phone_validator = RegexValidator(regex=r'^\+?\d{7,15}$', message='Invalid phone format.')

class Job(models.Model):
    EMP_TYPES = [
        ('full_time',  _('Full-time')),
        ('part_time',  _('Part-time')),
        ('contract',   _('Contract')),
        ('internship', _('Internship')),
        ('freelance',  _('Freelance')),
    ]
    title_ar  = models.CharField(max_length=255)
    title_en  = models.CharField(max_length=255, blank=True, default='')
    department = models.CharField(max_length=120, blank=True, default='')
    location_ar = models.CharField(max_length=160, blank=True, default='')
    location_en = models.CharField(max_length=160, blank=True, default='')
    employment_type = models.CharField(max_length=20, choices=EMP_TYPES, default='full_time')
    is_remote   = models.BooleanField(default=False)

    description_ar = models.TextField()
    description_en = models.TextField(blank=True, default='')
    requirements_ar = models.TextField(blank=True, default='')
    requirements_en = models.TextField(blank=True, default='')

    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency   = models.CharField(max_length=6, default='USD')

    apply_deadline = models.DateField(null=True, blank=True)
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title_en or self.title_ar

class JobApplication(models.Model):
    STATUS = [
        ('new',        'New'),
        ('shortlist',  'Shortlisted'),
        ('rejected',   'Rejected'),
        ('hired',      'Hired'),
    ]
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    full_name = models.CharField(max_length=120)
    email     = models.EmailField()
    phone     = models.CharField(max_length=20, validators=[phone_validator])
    cover_letter = models.TextField(blank=True, default='')
    portfolio_url = models.URLField(blank=True, default='')
    cv_file   = models.FileField(upload_to='careers/cv/', null=True, blank=True)
    status    = models.CharField(max_length=12, choices=STATUS, default='new')
    consent   = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['email']), models.Index(fields=['status']), models.Index(fields=['job'])]
