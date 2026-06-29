from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from core.models import TimeStampedModel

phone_validator = RegexValidator(
    regex=r'^09\d{9}$',
    message='شماره تماس باید با فرمت صحیح وارد شود'
)

class CustomUserManager(BaseUserManager):
    def _create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError('The number can not empty!')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)
        return user
    
    def create_user(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        return self._create_user(phone, password, **extra_fields)
    

class CustomUser(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    phone = models.CharField(
        verbose_name='شماره تماس',
        max_length=20,
        unique=True,
        validators= [phone_validator],
        help_text='شماره باید منحصر به فرد باشد'
    )
    first_name = models.CharField(
        verbose_name='نام',
        max_length=30
    )
    last_name = models.CharField(
        verbose_name='نام خانوادگی',
        max_length=30
    )
    email = models.EmailField(
        verbose_name='ایمیل',
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        default=True,
        help_text='مشخص میکند آیا کاربر فعال است یا نه'
    )
    is_staff = models.BooleanField(
        default=False,
        help_text='مربوط به دسترسی به پنل ادمین'
    )

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربرها'
        ordering = ['-created_at']

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'