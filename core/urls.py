from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


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
    # allauth
    path('accounts/', include('allauth.urls')),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

