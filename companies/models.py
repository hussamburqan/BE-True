from django.db import models

class Company(models.Model):
    name       = models.CharField(max_length=120)
    logo       = models.ImageField(upload_to='companies/', blank=True, null=True)
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name
