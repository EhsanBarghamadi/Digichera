from django import forms
from django.core.exceptions import ValidationError

from .models import Product, Category

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def value_from_datadict(self, data, files, name):
        upload = files.getlist(name)
        if not upload:
            return None
        return upload

class MultipleFileField(forms.ImageField):
    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ProductForm(forms.ModelForm):
    image = MultipleFileField(
        required=False,
        label='تصویر محصول',
        widget=MultipleFileInput(attrs={
            'class':'form-control',
            'multiple':True
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(is_active=True),
        label='دسته بندی',
        widget=forms.Select(attrs={
            'class':'form-control'
        }),
        empty_label='انتخاب دسته بندی'
    )
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'category']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'نام محصول'
                }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'توضیحات محصول'
                }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control', 
                }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control'
                }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['name'].disabled = True
            self.fields['name'].widget.attrs['class'] = 'form-control bg-light'
    
    def clean(self):
        cleaned_data = super().clean()
        files = self.cleaned_data.get('image') or []
        
        if len(files) > 3:
            self.add_error('image', 'شما نمی‌توانید بیشتر از ۳ تصویر برای محصول انتخاب کنید.')
            
        return cleaned_data