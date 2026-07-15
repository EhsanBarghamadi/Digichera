from django.db import models
from django.conf import settings

from core.models import TimeStampedModel

class Order(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = 'pending', 'در انتظار پرداخت'
        PAID = 'paid', 'پرداخت شده'
        SHIPPED = 'shipped', 'ارسال شده'
        DELIVERED = 'delivered', 'تحویل داده شده'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='کاربر'
    )
    store = models.ForeignKey(
        'store.Store',
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='فروشگاه'
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='وضعیت'
    )
    shipping_address = models.TextField(verbose_name='آدرس ارسال')

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'

    def __str__(self):
        return f'سفارش {self.pk} - {self.user}'

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    
class OrderItem(TimeStampedModel):
    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='سفارش ها'
    )
    product = models.ForeignKey(
        'product.Product',
        on_delete=models.PROTECT,
        related_name='order_items', 
        verbose_name='محصول'
    )
    product_name = models.CharField(
        max_length=255,
        verbose_name='نام محصول'
    )
    price = models.PositiveIntegerField(
        verbose_name='قیمت محصول'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='تعداد'
    )

    def __str__(self):
        return f'{self.product_name} × {self.quantity}'
    
    @property
    def total_price(self):
        return self.price * self.quantity

    