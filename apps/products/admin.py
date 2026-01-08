from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'image_preview', 'rating', 'catalog_type',)
    list_filter = ('category', 'catalog_type',)
    search_fields = ('name', 'description')
    list_editable = ('price','catalog_type',)

    def image_preview(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            try:
                return format_html(
                    '<img src="{}" width="64" height="64" style="object-fit: cover; border-radius: 4px;" />',
                    obj.image.url
                )
            except Exception as e:
                return f"Error: {str(e)}"
        return "Sin imagen"
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}