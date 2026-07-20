from django.urls import path

from . import views

app_name= 'store'

urlpatterns = [
    path('detail/', views.store_detail, name='detail'),
    path('create/', views.store_create, name='create'),
    path('update/', views.store_update, name='update'),
]