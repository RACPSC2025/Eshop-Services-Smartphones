"""
Context processor para exponer configuración de PayPal a los templates.
Permite usar {{ PAYPAL_CLIENT_ID }} directamente en cualquier template.
"""
from django.conf import settings


def paypal_settings(request):
    """
    Expone las credenciales de PayPal necesarias para el SDK de JavaScript.
    
    Returns:
        dict: Diccionario con PAYPAL_CLIENT_ID y PAYPAL_MODE
    """
    return {
        'PAYPAL_CLIENT_ID': str(settings.PAYPAL_CLIENT_ID).strip('"'),
        'PAYPAL_MODE': str(settings.PAYPAL_MODE).strip('"'),
    }
