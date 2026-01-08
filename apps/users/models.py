from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField

class Profile(models.Model):
    """Perfil extendido del usuario para información adicional"""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Usuario'
    )
    
    # Información personal
    phone = models.CharField('Teléfono', max_length=20, blank=True)
    document_type = models.CharField(
        'Tipo de documento',
        max_length=10,
        choices=[
            ('CC', 'Cédula de Ciudadanía'),
            ('CE', 'Cédula de Extranjería'),
            ('TI', 'Tarjeta de Identidad'),
            ('PASS', 'Pasaporte'),
        ],
        blank=True
    )
    document_number = models.CharField('Número de documento', max_length=20, blank=True)
    birth_date = models.DateField('Fecha de nacimiento', null=True, blank=True)
    
    # Dirección por defecto
    address = models.TextField('Dirección', blank=True)
    city = models.CharField('Ciudad', max_length=100, blank=True)
    department = models.CharField('Departamento', max_length=100, blank=True)
    postal_code = models.CharField('Código postal', max_length=10, blank=True)
    country = models.CharField('País', max_length=50, default='Colombia')
    
    # Imagen de perfil
    avatar = CloudinaryField(
        'Foto de perfil',
        blank=True,
        null=True
    )
    
    # Preferencias
    newsletter_subscription = models.BooleanField(
        'Suscrito a newsletter',
        default=False
    )
    email_notifications = models.BooleanField(
        'Notificaciones por email',
        default=True
    )
    
    # Timestamps
    created_at = models.DateTimeField('Fecha de registro', auto_now_add=True)
    updated_at = models.DateTimeField('Última actualización', auto_now=True)
    
    class Meta:
        verbose_name = 'Perfil de usuario'
        verbose_name_plural = 'Perfiles de usuarios'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Perfil de {self.user.username}"
    
    def get_full_name(self):
        """Retorna el nombre completo del usuario"""
        return self.user.get_full_name() or self.user.username
    
    def has_complete_shipping_info(self):
        """Verifica si el usuario tiene información de envío completa"""
        return all([
            self.phone,
            self.address,
            self.city,
        ])


# Signals para crear automáticamente el perfil cuando se crea un usuario
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crea automáticamente un perfil cuando se crea un usuario"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Guarda el perfil cuando se guarda el usuario"""
    if hasattr(instance, 'profile'):
        instance.profile.save()

