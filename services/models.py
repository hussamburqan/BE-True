from django.db import models

class Service(models.Model):
    title_ar       = models.CharField(max_length=255)
    title_en       = models.CharField(max_length=255)
    description_ar = models.TextField()
    description_en = models.TextField()
    icon           = models.ImageField(upload_to='service/', blank=True, null=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title_en or self.title_ar
