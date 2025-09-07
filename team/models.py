from django.db import models
from django.utils.text import slugify

class TeamMember(models.Model):
    name   = models.CharField(max_length=120)
    title  = models.CharField(max_length=120, blank=True, default="")

    photo  = models.ImageField(upload_to="team/", blank=True, null=True)

    facebook  = models.URLField(blank=True, default="")
    twitter   = models.URLField(blank=True, default="")
    instagram = models.URLField(blank=True, default="")
    linkedin  = models.URLField(blank=True, default="")
    website   = models.URLField(blank=True, default="")

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name", "id"]

    def __str__(self):
        return self.name
