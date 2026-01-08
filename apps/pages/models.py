from django.db import models
from django.contrib.auth.models import User

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
