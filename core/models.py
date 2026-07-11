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
        raise NotImplementedError("Subclasses must implement get_source_field()")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            source_field_name = self.get_source_field()
            source_value = getattr(self, source_field_name, '')
            if source_value:
                base_slug = slugify(source_value, allow_unicode=True)
                slug = base_slug
                counter = 1
                model_class = self.__class__
                while model_class.objects.filter(slug=slug).exists():
                    slug = f'{base_slug}-{counter}'
                    counter += 1
                self.slug = slug
        super().save(*args, **kwargs)