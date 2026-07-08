import os
from io import BytesIO

from django.db import models
from django.conf import settings
from PIL import Image
from localflavor.ir.forms import IRPostalCodeField
from django.core.files.base import ContentFile

from core.models import TimeStampedModel
from .validators import validate_file_size

class Profile(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='کاربر'
    )
    location = models.TextField(
        verbose_name='آدرس',
        max_length=255,
        blank=True,
        null=True,
    )
    postal_code = models.CharField(
        verbose_name='کد پستی',
        max_length=10,
        validators=[IRPostalCodeField().clean],
        blank=True,
        null=True,
    )
    avatar = models.ImageField(
        verbose_name='تصویر پروفایل',
        upload_to='avatars/',
        validators=[validate_file_size],
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل ها'

    def __str__(self):
        full_name = f"{self.user.first_name} {self.user.last_name}".strip()


    def save(self, *args, **kwargs):
        if self.avatar:
            img = Image.open(self.avatar)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.thumbnail((300, 300), Image.LANCZOS)
            output = BytesIO()
            img.save(output, format='JPEG', quality=70)
            output.seek(0)

            self.avatar.save(
                os.path.basename(self.avatar.name),
                ContentFile(output.read()),
                save=False
            )
        super().save(*args, **kwargs)