from django.db import models
from django.conf import settings

from core.models import TimeStampedModel

class Cart(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        null=True,
        blank=True,
        verbose_name='کاربر'
    )
    session_key = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        verbose_name='شناسه نشست مهمان'
    )

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد های خرید'

    def __str__(self):
        return f'سبد {self.user}' if self.user else f'سبد مهمان {self.session_key}'

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())
    

class CartItem(TimeStampedModel):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='سبد خرید'
    )
    product = models.ForeignKey(
        'product.Product',
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='محصول'
    )
    quantity = models.PositiveBigIntegerField(
        default=1,
        verbose_name='تعداد'
    )

    class Meta:
        verbose_name = 'آیتم سبد خرید'
        verbose_name_plural = 'آیتم سبد خرید'
        unique_together = ('cart', 'product')

    def __str__(self):
       return f'{self.product.name} × {self.quantity}'
    
    @property
    def total_price(self):
        return self.product.price * self.quantity
