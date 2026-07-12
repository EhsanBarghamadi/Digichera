from django.urls import path

from .views import profile_view, profile_edit

app_name = 'account'

urlpatterns = [
        path('profile/', profile_view, name='profile'),
        path('profile_edit/', profile_edit, name='profile_edit'),
]