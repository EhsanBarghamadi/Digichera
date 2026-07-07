from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('phone', 'first_name', 'last_name', 'is_active', 'is_staff')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'رمز عبور'
        self.fields['password2'].label = 'تکرار رمز عبور'

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('phone', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')