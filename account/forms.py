from django import forms
from localflavor.ir.forms import IRPostalCodeField

from .models import Profile

class ProfileForm(forms.ModelForm):
    postal_code = IRPostalCodeField(
        max_length=10,
        min_length=10,
        label='کد پستی',
        widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'کد پستی خود را وارد کنید',
        }),
    )
    
    class Meta:
        model = Profile
        fields = ['avatar', 'location', 'postal_code']
        labels = {
            'avatar': 'تصویر پروفایل',
            'location': 'آدرس محل سکونت',
        }
        widgets = {
            'avatar': forms.FileInput(attrs={
                'class': 'form_control_file',
            }),
            'location': forms.Textarea(attrs={
                'class': 'single-textarea',
                'placeholder': 'آدرس خود را وارد کنید',
            }),
        }