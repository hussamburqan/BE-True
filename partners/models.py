# app/models.py
from django.db import models


class Partner(models.Model):
    name_ar        = models.CharField(max_length=120)
    name_en        = models.CharField(max_length=120)
    description_ar = models.TextField(blank=True, default="")
    description_en = models.TextField(blank=True, default="")
    website        = models.URLField(blank=True)
    logo           = models.ImageField(upload_to='partners/', blank=True, null=True)
    is_active      = models.BooleanField(default=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name_ar or self.name_en
