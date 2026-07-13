import os
from io import BytesIO
from PIL import Image

from django.db import models
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError

from core.models import SluggedModel, TimeStampedModel
from .validators import validate_file_size

class Category(SluggedModel):
    name = models.CharField(
        verbose_name='نام دسته بندی',
        max_length=255,
        unique=True
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='دسته بندی والد'
    )
    is_active = models.BooleanField(
        verbose_name='فعال بودن',
        default=True
    )

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def get_source_field(self):
        return 'name'
    
    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()
        for child in self.children.all():
            child.delete()

    def clean(self):
        if self.parent:
            p = self.parent
            while p:
                if p == self:
                    raise ValidationError('یک دسته‌بندی نمی‌تواند زیرمجموعه‌ی خودش باشد.')
                p = p.parent 
        return super().clean()

class ProductImage(TimeStampedModel):
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='محصول'
    )
    image = models.ImageField(
        verbose_name='تصویر محصول',
        upload_to='product/%Y/%m/%d/',
        validators=[validate_file_size]
    )
    title = models.CharField(
        verbose_name='عنوان',
        max_length=30
    )
    is_primary = models.BooleanField(
        verbose_name='عکس اصلی',
        default=False
    )

    class Meta:
        verbose_name = 'تصویر محصول'
        verbose_name_plural = 'تصویر محصولات'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        should_process_image = False

        if self.image:
            if not self.pk:
                should_process_image = True
            else:
                try:
                    old_instance = self.__class__.objects.get(pk=self.pk)
                    if old_instance.image != self.image:
                        should_process_image = True
                except self.__class__.DoesNotExist:
                    should_process_image = True

        if should_process_image and self.image:
            img = Image.open(self.image)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.thumbnail((600, 600), Image.LANCZOS)
            output = BytesIO()
            img.save(output, format='JPEG', quality=70, optimize=True)
            output.seek(0)

            self.image.save(
                os.path.basename(self.image.name),
                ContentFile(output.read()),
                save=False
            )
        super().save(*args, **kwargs)


class Product(SluggedModel):
    store = models.ForeignKey(
        "store.Store",
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='فروشگاه'
    )
    category = models.ForeignKey(
        "Category",
        related_name='products',
        on_delete=models.PROTECT
    )
    name = models.CharField(
        verbose_name='نام محصول',
        max_length=255
    )
    description = models.TextField(
        verbose_name='توضیحات'
    )
    price = models.PositiveIntegerField(
        verbose_name='قیمت'
    )
    stock = models.PositiveIntegerField(
        verbose_name='موجودی انبار'
    )
    is_active = models.BooleanField(
        verbose_name='وضعیت',
        default=True
    )

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ['store']

    def __str__(self):
        return self.name
    
    def get_source_field(self):
        return 'name'
    
