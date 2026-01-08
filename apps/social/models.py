from django.db import models
from cloudinary.models import CloudinaryField

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

class SocialMedia(models.Model):
    """
    Modelo para gestionar enlaces a redes sociales
    - Iconos personalizables (Font Awesome, etc.)
    - Plataformas únicas para evitar duplicados
    - Sistema de activación/desactivación
    """
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter/X'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
        ('whatsapp', 'WhatsApp'),
        ('telegram', 'Telegram'),
        ('linkedin', 'LinkedIn'),
        ('github', 'GitHub'),
        ('discord', 'Discord'),
    ]
    
    platform = models.CharField(
        max_length=50, 
        choices=PLATFORM_CHOICES, 
        unique=True, 
        verbose_name="plataforma"
    )
    url = models.URLField(verbose_name="URL")
    icon = models.CharField(max_length=50, verbose_name="icono")
    is_active = models.BooleanField(default=True, verbose_name="activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="fecha de actualización")
    
    class Meta:
        verbose_name = "red social"
        verbose_name_plural = "redes sociales"
        ordering = ['platform']
    
    def __str__(self):
        return f"{self.get_platform_display()} - {self.url}"
    
    def save(self, *args, **kwargs):
        """Asignar icono automático si no se proporciona"""
        if not self.icon:
            # Iconos por defecto usando Font Awesome
            icon_map = {
                'facebook': 'fab fa-facebook',
                'twitter': 'fab fa-twitter',
                'instagram': 'fab fa-instagram',
                'youtube': 'fab fa-youtube',
                'tiktok': 'fab fa-tiktok',
                'whatsapp': 'fab fa-whatsapp',
                'telegram': 'fab fa-telegram',
                'linkedin': 'fab fa-linkedin',
                'github': 'fab fa-github',
                'discord': 'fab fa-discord',
            }
            self.icon = icon_map.get(self.platform, 'fas fa-link')
        super().save(*args, **kwargs)