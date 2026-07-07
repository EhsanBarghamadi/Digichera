from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreateAdminForm, CustomUserChangeAdminForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreateAdminForm
    form = CustomUserChangeAdminForm

    list_display = ('first_name', 'last_name', 'phone', 'is_staff', 'is_active')
    ordering = ('-created_at',)
    search_fields = ("phone", "first_name", "last_name",)
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    filter_horizontal = ('groups', 'user_permissions')
    list_editable = ('is_active',)
    
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'first_name', 'last_name', 'email', 'role', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )

