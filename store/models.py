import os
from io import BytesIO
from PIL import Image

from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile

from core.models import SluggedModel
from .validators import validate_file_size

class Store(SluggedModel):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='store',
        verbose_name='مالک فروشگاه'
    )
    store_name = models.CharField(
        verbose_name='اسم فروشگاه',
        max_length=255,
    )
    store_logo = models.ImageField(
        verbose_name='لوگوی فروشگاه',
        upload_to='store_logo/%Y/%m/%d/',
        validators=[validate_file_size],
        blank=True,
        null=True
    )
    store_phone = models.CharField(
        verbose_name='شماره تماس فروشگاه',
        max_length=20,
        unique=True
    )
    is_active = models.BooleanField(
        verbose_name='فعال بودن فروشگاه',
        default=True
    )

    class Meta:
        verbose_name = 'فروشگاه'
        verbose_name_plural = 'فروشگاه ها'
        ordering = ['-created_at']

    def __str__(self):
        return self.store_name

    def get_source_field(self):
        return 'store_name'
    
    def save(self, *args, **kwargs):
        should_process_logo = False

        if self.store_logo:
            if not self.pk:
                should_process_logo = True
            else:
                try:
                    old_instance = self.__class__.objects.get(pk=self.pk)
                    if old_instance.store_logo != self.store_logo:
                         should_process_logo = True
                except self.__class__.DoesNotExist:
                    should_process_logo = True

        if should_process_logo and self.store_logo:
            img = Image.open(self.store_logo)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.thumbnail((300, 300), Image.LANCZOS)
            output = BytesIO()
            img.save(output, format='JPEG', quality=70)
            output.seek(0)
            
            self.store_logo.save(
                os.path.basename(self.store_logo.name),
                ContentFile(output.read()),
                save=False
            )
        super().save(*args, **kwargs)