# apps/payment/urls.py
from django.urls import path
from .views import create_paypal_order, capture_paypal_order

urlpatterns = [
    # Crear orden en PayPal
    path('create/', create_paypal_order, name='paypal-create'),
    # Capturar orden después de aprobación
    path('capture/<str:order_id>/', capture_paypal_order, name='paypal-capture'),
]