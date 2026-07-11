from django.contrib import admin

from .models import Store

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['store_name', 'owner', 'store_logo', 'is_active']
    list_editable = ['is_active']
    ordering = ['created_at']
    readonly_fields = ['slug']
