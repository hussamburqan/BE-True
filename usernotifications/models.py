from django.db import models
from django.conf import settings
from django.utils import timezone

class Notification(models.Model):
    """
    إشعار بسيط موجه لمستخدم واحد.
    """
    user        = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    title       = models.CharField(max_length=255)
    body        = models.TextField(blank=True)
    is_read     = models.BooleanField(default=False)

    created_at  = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} – {self.title[:60]}"
