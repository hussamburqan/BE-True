from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


phone_validator = RegexValidator(
    regex=r'^\+?\d{7,15}$',
    message='Invalid phone format.'
)


class BaseStamped(models.Model):
    """Abstract base with created_at ordering + common indexes."""
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class TalentApplication(BaseStamped):
    STATUS = [
        ('new',       _('New')),
        ('shortlist', _('Shortlisted')),
        ('rejected',  _('Rejected')),
        ('hired',     _('Hired')),
    ]

    full_name     = models.CharField(max_length=120)
    email         = models.EmailField()
    phone         = models.CharField(max_length=20, validators=[phone_validator])

    cover_letter  = models.TextField(blank=True, default='')
    portfolio_url = models.URLField(blank=True, default='')
    cv_file       = models.FileField(upload_to='careers/talent_cv/', null=True, blank=True)

    consent       = models.BooleanField(default=False)  
    answers       = models.JSONField(default=dict, blank=True) 

    status        = models.CharField(max_length=12, choices=STATUS, default='new')

    class Meta(BaseStamped.Meta):
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class InternshipApplication(BaseStamped):
    """Dedicated model for university field training applications."""
    STATUS = [
        ('new',        _('New')),
        ('shortlist',  _('Shortlisted')),
        ('interview',  _('Interview')),
        ('accepted',   _('Accepted')),
        ('rejected',   _('Rejected')),
    ]

    full_name   = models.CharField(max_length=120)
    email       = models.EmailField()
    phone       = models.CharField(max_length=20, validators=[phone_validator])

    university  = models.CharField(max_length=160, blank=True, default='')
    major       = models.CharField(max_length=160, blank=True, default='')
    study_level = models.CharField(max_length=80, blank=True, default='')

    DURATION = [
        ('1m', _('1 month')),
        ('2m', _('2 months')),
        ('3m', _('3 months')),
        ('other', _('Other')),
    ]
    duration    = models.CharField(max_length=8, choices=DURATION, default='1m')

    TRACK = [
        ('marketing', _('Digital Marketing')),
        ('design',    _('Graphic Design')),
        ('content',   _('Content Creation')),
        ('photo',     _('Photography & Video')),
        ('other',     _('Other')),
    ]
    track       = models.CharField(max_length=20, choices=TRACK, default='marketing')

    experience_text = models.TextField(blank=True, default='')
    goal            = models.TextField(blank=True, default='')
    strengths       = models.TextField(blank=True, default='')
    teamwork        = models.CharField(max_length=16, blank=True, default='')
    challenge       = models.TextField(blank=True, default='')

    portfolio_url = models.URLField(blank=True, default='')
    cv_file       = models.FileField(upload_to='careers/intern_cv/', null=True, blank=True)
    consent       = models.BooleanField(default=False)
    answers       = models.JSONField(default=dict, blank=True)

    status        = models.CharField(max_length=12, choices=STATUS, default='new')

    class Meta(BaseStamped.Meta):
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['status']),
            models.Index(fields=['university']),
            models.Index(fields=['track']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"[Internship] {self.full_name} ({self.email})"
