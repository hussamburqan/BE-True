from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

class Course(models.Model):

    title_ar = models.CharField(max_length=255, db_index=True)
    title_en = models.CharField(max_length=255, blank=True, default='', db_index=True)
    slug     = models.SlugField(max_length=255, blank=True, default='', db_index=True, help_text=_('Optional SEO slug'))

    description_ar = models.TextField(blank=True, default='')
    description_en = models.TextField(blank=True, default='')
    curriculum_ar  = models.TextField(blank=True, default='')
    curriculum_en  = models.TextField(blank=True, default='')

    image      = models.ImageField(upload_to='course_images/', blank=True, null=True)
    instructor_photo   = models.ImageField(upload_to='course_instructors/', blank=True, null=True)

    price     = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_index=True)
    currency  = models.CharField(max_length=6, default='ILS')

    start_date = models.DateField(blank=True, null=True, db_index=True)
    end_date   = models.DateField(blank=True, null=True)
    registration_end_date = models.DateField(blank=True, null=True, db_index=True)

    instructor_name_ar = models.CharField(max_length=120, blank=True, default='')
    instructor_name_en = models.CharField(max_length=120, blank=True, default='')

    class AttendanceMode(models.TextChoices):
        IN_PERSON = 'in_person',
        ONLINE    = 'online',
        HYBRID    = 'hybrid',

    attendance_mode = models.CharField(max_length=16, choices=AttendanceMode.choices, default=AttendanceMode.IN_PERSON)
    location_ar     = models.CharField(max_length=160, blank=True, default='')
    location_en     = models.CharField(max_length=160, blank=True, default='')

    capacity      = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    certificate_included = models.BooleanField(default=False)

    is_online  = models.BooleanField(default=False)
    is_active  = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['attendance_mode']),
            models.Index(fields=['is_active']),
            models.Index(fields=['slug']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(capacity__isnull=True) | models.Q(capacity__gte=1),
                name='course_capacity_positive'
            ),
        ]

    def __str__(self):
        return self.title_en or self.title_ar

    @property
    def registration_open(self) -> bool:
        """
        اعتبر التسجيل مفتوح إذا الدورة فعّالة ولم ينتهِ تسجيلها بعد
        (ولو في capacity تقدر تضيف منطق التتبع لاحقًا).
        """
        from django.utils import timezone
        if not self.is_active:
            return False
        if self.registration_end_date:
            return timezone.now().date() <= self.registration_end_date
        return True
