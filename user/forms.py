from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser

class CustomUserCreateAdminForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('phone', 'first_name', 'last_name', 'role', 'is_active', 'is_staff')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'رمز عبور'
        self.fields['password2'].label = 'تکرار رمز عبور'

class CustomUserChangeAdminForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('phone', 'first_name', 'last_name', 'role', 'is_active', 'is_staff', 'is_superuser')

class CustomUserCreateForm(forms.ModelForm):

    ROLE_CHOICES = [
        ('customer', 'کاربر عادی'),
        ('seller', 'فروشنده'),
    ]
    role = forms.ChoiceField(
            choices=ROLE_CHOICES,
            widget=forms.Select(attrs={
                'class': 'form-control current',
                'placeholder': 'نقش'
            }),
            label='نقش',
        )
    password = forms.CharField(
            widget=forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'رمز عبور'
            }),
            label='رمز عبور'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'تکرار رمز عبور'
        }),
        label='تکرار رمز عبور'
    )

    class Meta:
        model = CustomUser
        fields = ('phone', 'first_name', 'last_name', 'role')
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'تلفن همراه'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام خانوادگی'
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if CustomUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError('این شماره تلفن قبلاً ثبت شده است.')
        return phone
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('رمز عبور با تکرار آن مطابقت ندارد!')
        if password:
            validate_password(password)
        return cleaned_data

class CustomUserLoginForm(forms.Form):
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'شماره تلفن'
            }
        ),
        label='شماره تلفن'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'رمز عبور'
            }
        ),
        label='رمز عبور'
    )