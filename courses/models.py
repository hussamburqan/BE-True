from django.db import models

class Course(models.Model):
    title_ar = models.CharField(max_length=255, db_index=True)
    title_en = models.CharField(max_length=255, blank=True, default='', db_index=True)
    description_ar = models.TextField(blank=True, default='')
    description_en = models.TextField(blank=True, default='')
    curriculum_ar  = models.TextField(blank=True, default='')
    curriculum_en  = models.TextField(blank=True, default='')

    image      = models.ImageField(upload_to='course_images/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_index=True)
    start_date = models.DateField(blank=True, null=True, db_index=True)
    end_date   = models.DateField(blank=True, null=True)
    registration_end_date = models.DateField(blank=True, null=True, db_index=True)

    instructor_name_ar = models.CharField(max_length=120, blank=True, default='')
    instructor_name_en = models.CharField(max_length=120, blank=True, default='')
    instructor_photo   = models.ImageField(upload_to='course_instructors/', blank=True, null=True)
    
    is_online  = models.BooleanField(default=False)
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title_en or self.title_ar
