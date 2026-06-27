from django.db import models
from django.utils.text import slugify

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاریخ بروزرسانی'
    )

    class Meta:
        abstract = True

class SluggedModel(TimeStampedModel):
    slug = models.SlugField(
        max_length=255,
        unique=True,
        allow_unicode=True,
        verbose_name='اسلاگ'
    )

    class Meta:
        abstract = True

    def get_source_field(self):
        raise NotImplementedError("Subclasses must implement get_slug_source_field()")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            source_field_name = self.get_source_field()
            source_value = getattr(self, source_field_name, '')
            if source_value:
                self.slug = slugify(source_value, allow_unicode=True)
        super().save(*args, **kwargs)