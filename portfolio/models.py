from django.db import models

class PortfolioItem(models.Model):
    title_ar = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    link = models.TextField(null=True)
    image_cover = models.ImageField(upload_to='portfolio/covers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title_en or self.title_ar
