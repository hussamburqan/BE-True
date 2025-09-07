from django.db import models
from django.conf import settings

class AuditLog(models.Model):
    ACTION_CREATE  = "create"
    ACTION_UPDATE  = "update"
    ACTION_DELETE  = "delete"
    ACTION_LOGIN   = "login"
    ACTION_LOGOUT  = "logout"
    ACTION_CUSTOM  = "custom"

    ACTION_CHOICES = [
        (ACTION_CREATE, ACTION_CREATE),
        (ACTION_UPDATE, ACTION_UPDATE),
        (ACTION_DELETE, ACTION_DELETE),
        (ACTION_LOGIN,  ACTION_LOGIN),
        (ACTION_LOGOUT, ACTION_LOGOUT),
        (ACTION_CUSTOM, ACTION_CUSTOM),
    ]

    actor       = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="audit_logs")
    action      = models.CharField(max_length=16, choices=ACTION_CHOICES)
    app_label   = models.CharField(max_length=64)
    model       = models.CharField(max_length=64)
    object_pk   = models.CharField(max_length=64, blank=True, default="")
    object_repr = models.CharField(max_length=255, blank=True, default="")

    route       = models.CharField(max_length=255, blank=True, default="")
    method      = models.CharField(max_length=8,  blank=True, default="")
    ip_address  = models.CharField(max_length=45, blank=True, default="") 
    user_agent  = models.TextField(blank=True, default="")

    changes     = models.JSONField(null=True, blank=True)
    extra       = models.JSONField(null=True, blank=True)

    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["app_label", "model"]),
            models.Index(fields=["action"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        who = self.actor_id or "system"
        return f"[{self.action}] {self.app_label}.{self.model}({self.object_pk}) by {who} @ {self.created_at:%Y-%m-%d %H:%M}"
