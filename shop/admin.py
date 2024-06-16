from django.contrib import admin
from .models import ProductCategory, Manufacturer, Product


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_visible', 'sort']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'manufacturer', 'is_visible']
    list_filter = ['category', 'manufacturer']
    search_fields = ['name', 'description']
