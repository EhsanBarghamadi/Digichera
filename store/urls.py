from django.urls import path

from . import views

app_name= 'store'

urlpatterns = [
    path('create/', views.store_create, name='create'),
]