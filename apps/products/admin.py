from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'rating')
    list_filter = ('category', 'subcategory')
    search_fields = ('name', 'description')