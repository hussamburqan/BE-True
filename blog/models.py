from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

def unique_slugify(instance, value, slug_field_name="slug", max_length=255):
    base_slug = slugify(value)[:max_length]
    slug = base_slug
    ModelClass = instance.__class__
    i = 2
    while ModelClass.objects.filter(**{slug_field_name: slug}).exclude(pk=instance.pk).exists():
        suffix = f"-{i}"
        slug = (base_slug[:max_length - len(suffix)]) + suffix
        i += 1
    return slug

class Post(models.Model):
    title_ar   = models.CharField(max_length=255)
    title_en   = models.CharField(max_length=255)
    slug       = models.SlugField(max_length=300, unique=True, blank=True)

    content_ar = RichTextField(blank=True)
    content_en = RichTextField(blank=True)

    cover      = models.ImageField(upload_to='blog/covers/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        base_title = self.title_en or self.title_ar or "post"
        if not self.slug:
            self.slug = unique_slugify(self, base_title, max_length=300)
        else:
            self.slug = unique_slugify(self, self.slug, max_length=300)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title_en or self.title_ar
