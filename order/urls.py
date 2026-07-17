from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.order_success, name='success'),
    path('<int:order_id>/update-status/', views.order_update_status, name='update_status'),
]