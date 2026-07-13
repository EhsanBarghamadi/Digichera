from django.contrib import admin

from .models import Category, ProductImage, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_active')
    list_filter = ('is_active', 'parent')
    readonly_fields = ('slug',)
    actions = None

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'title', 'is_primary', 'created_at')
    list_filter = ('created_at', 'is_primary')
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('store', 'name', 'category', 'price', 'stock', 'is_active')
    list_filter = ('is_active', 'created_at')
    readonly_fields = ('slug',)
