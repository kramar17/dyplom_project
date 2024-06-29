from django.contrib import admin
from .models import ProductCategory, Manufacturer, Product, Order


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for ProductCategory model.
    """
    list_display = ['name', 'slug', 'is_visible', 'sort']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    """
    Admin configuration for Manufacturer model.
    """
    list_display = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for Product model.
    """
    list_display = ['name', 'price', 'category', 'manufacturer', 'is_visible']
    list_filter = ['category', 'manufacturer']
    search_fields = ['name', 'description']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for Order model.
    """
    list_display = ('id', 'user', 'first_name', 'last_name', 'total_price', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone_number', 'first_name', 'last_name')
