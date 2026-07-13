from django.urls import path

from .views import create_store

app_name= 'store'

urlpatterns = [
    path('create/', create_store, name='create'),
]