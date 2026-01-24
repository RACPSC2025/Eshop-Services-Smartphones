from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django_ckeditor_5.fields import CKEditor5Field


class Banner(models.Model):
    """
    Modelo para gestionar banners promocionales
    - Imágenes almacenadas en Cloudinary
    - Posicionamiento para ordenar banners
    - Enlaces personalizables para campañas
    """
    title = models.CharField(max_length=255, verbose_name="título")
    image = CloudinaryField('banners/', null=True, default=None)
    link = models.URLField(blank=True, null=True, verbose_name="enlace")
    is_active = models.BooleanField(default=True, verbose_name="activo")
    position = models.IntegerField(default=0, verbose_name="posición")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="fecha de actualización")
    
    class Meta:
        verbose_name = "banner"
        verbose_name_plural = "banners"
        ordering = ['position', '-created_at']
    
    def __str__(self):
        return f"{self.title} ({'Activo' if self.is_active else 'Inactivo'})"


class About(models.Model):
    title_info = models.CharField(max_length=255, verbose_name="título", help_text="Título de la información de la empresa. Ej.: Misión, Visión, Valores")
    content = CKEditor5Field(
       'Content',
       config_name='default',
       blank=True,
       null=True
   )

    is_active = models.BooleanField(default=True, verbose_name="activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="fecha de actualización")
    
    class Meta:
        verbose_name = "acerca de"
        verbose_name_plural = "acerca de"
    
    def __str__(self):
        return "Información sobre la empresa"


class Testimonial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='testimonials', verbose_name="usuario")
    order = models.OneToOneField('orders.Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='testimonial', verbose_name="pedido")
    comment = models.TextField(verbose_name="comentario")
    rating = models.PositiveSmallIntegerField(default=5, verbose_name="calificación")  # 1-5 stars
    is_active = models.BooleanField(default=True, verbose_name="¿está activo?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="fecha de creación")

    class Meta:
        verbose_name = 'Testimonio'
        verbose_name_plural = 'Testimonios'
        ordering = ['-created_at']

    def __str__(self):
        return f"Testimonio de {self.user.username} ({self.rating} estrellas)"
