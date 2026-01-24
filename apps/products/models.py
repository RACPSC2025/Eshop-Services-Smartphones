from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="nombre de la categoría")
    additional_info = models.TextField(verbose_name="información adicional", blank=True, null=True)
    slug = models.SlugField(unique=True, verbose_name="slug")
    is_active = models.BooleanField(default=True, verbose_name="¿está activo?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="fecha de actualización")
    
    class Meta:
        verbose_name = "categoría"
        verbose_name_plural = "categorías"
    
    def __str__(self):
        return self.name

class Product(models.Model):

    class CatalogType(models.TextChoices):
        PRODUCT = 'PRODUCT', 'Producto'
        SERVICE = 'SERVICE', 'Servicio'

    name = models.CharField(max_length=255, verbose_name="nombre")
    description = models.TextField(verbose_name="descripción", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="precio")
    image = CloudinaryField('Imagen', null=True, default=None, blank=True) 
    catalog_type = models.CharField(max_length=100, blank=True, choices=CatalogType.choices, verbose_name="tipo de catálogo")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="categoría")
    tag = models.CharField(max_length=50, blank=True, verbose_name="etiqueta")
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True, verbose_name="calificación")

    class Meta:
        verbose_name = "producto"
        verbose_name_plural = "productos"

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class FileResource(models.Model):
    title = models.CharField(max_length=255, verbose_name="título")
    file = models.FileField(upload_to='file_resources/', null=True, default=None)
    is_active = models.BooleanField(default=True, verbose_name="activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="fecha de actualización")
    
    class Meta:
        verbose_name = "archivo"
        verbose_name_plural = "archivos"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({'Activo' if self.is_active else 'Inactivo'})"
    