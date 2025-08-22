from django.db import models
from django.conf import settings
from django.utils import timezone


class SystemLog(models.Model):
    """
    يسجّل أحداثًا مهمّة (تسجيل دخول، تغيير حالة، أخطاء، إلخ).
    """
    LEVEL_CHOICES = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    ]

    level       = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='info')
    message     = models.TextField()
    actor       = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name='system_logs')
    created_at  = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"[{self.level.upper()}] {self.message[:60]}"
