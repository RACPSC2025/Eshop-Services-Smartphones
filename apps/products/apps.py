from django.apps import AppConfig


class ProductsConfig(AppConfig):
    name = 'apps.products'

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
