from django.db import models
from django.conf import settings

class UploadedFile(models.Model):
    file         = models.FileField(upload_to='uploads/%Y/%m/')
    original_name = models.CharField(max_length=255)
    size         = models.PositiveBigIntegerField()
    content_type = models.CharField(max_length=100, blank=True)

    uploaded_by  = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='uploaded_files',
    )
    uploaded_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_name
