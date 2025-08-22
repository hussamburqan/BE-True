from django.db import models

class PortfolioItem(models.Model):
    title       = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image       = models.ImageField(upload_to='portfolio/', blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
