from django import forms

from .models import Store
from .validators import validate_landline_phone

class StoreForm(forms.ModelForm):
    store_phone = forms.CharField(
        validators=[validate_landline_phone],
        max_length=11,
        min_length=11,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'شماره تماس ثابت فروشگاه را وارد کنید',
        }),
        label='شماره تماس فروشگاه'
    )
    class Meta:
        model = Store
        fields = ['store_name', 'store_phone', 'store_logo']
        labels = {
            'store_name': 'نام فروشگاه',
            'store_logo': 'لوگوی فروشگاه'
        }
        widgets = {
            'store_logo': forms.FileInput(attrs={
                'class': 'form_control_file',
            }),
            'store_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام فروشگاه را وارد کنید',
            }),
        }