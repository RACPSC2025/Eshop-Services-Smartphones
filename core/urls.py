from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Incluye las páginas. El string vacío '' hace que sea la página de inicio.
    path('', include('apps.pages.urls')), 
    
    # Tu app de productos que ya tenías
    path('products/', include('apps.products.urls')),
]
