from django.urls import path

from . import views

app_name = 'product'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('search/', views.product_search, name='search'),
    path('category/<int:category_id>', views.product_category, name='category'),
    path('create/', views.product_create, name='product_create'),
    path('products/<str:slug>/', views.product_detail, name='product_detail'),
    path('<int:pk>/update/', views.product_update, name='product_update'),
]