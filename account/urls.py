from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
        path('', views.profile_detail, name='detail'),
        path('update/', views.profile_update, name='update'),
]