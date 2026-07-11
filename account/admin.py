from django.contrib import admin

from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','location', 'postal_code', 'avatar', 'created_at', 'updated_at')
    raw_id_fields = ('user', )
    list_filter = ('created_at',)

