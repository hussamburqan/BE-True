from django.db import models

RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

class Testimonial(models.Model):
    name    = models.CharField(max_length=120)
    role    = models.CharField(max_length=160, blank=True)
    company = models.CharField(max_length=160, blank=True)
    avatar  = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating  = models.IntegerField(choices=RATING_CHOICES, default=5)
    comment_ar = models.TextField()
    comment_en = models.TextField()
    is_active   = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  

    class Meta:
        ordering = ['-created_at', 'id'] 

    def __str__(self):
        return f"{self.name} ({self.company})"
