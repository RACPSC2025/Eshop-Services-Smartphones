from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    # Home y Páginas Estaticas
    path('', include('apps.pages.urls')), 
    # app de productos
    path('products/', include('apps.products.urls')),
    # app de usuarios
    path('users/', include('apps.users.urls')),
    # app de pedidos
    path('orders/', include('apps.orders.urls')),
]
