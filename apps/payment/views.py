from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
import requests

from .models import Transaction


def create_paypal_order(request):
    """
    Crea una orden en PayPal. Si se reciben datos de envío, los guarda en sesión.
    Esto permite unificar la validación de checkout y creación de orden en un solo viaje.
    """
    from apps.orders.models import Cart
    from apps.orders.forms import CheckoutForm
    
    # 1. Validar usuario y carrito
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Debes iniciar sesión'}, status=403)
        
    try:
        cart = Cart.objects.get(user=request.user)
        if cart.get_total_items() == 0:
            return JsonResponse({'success': False, 'error': 'Carrito vacío'}, status=400)
    except Cart.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Carrito no encontrado'}, status=404)

    # 2. Si vienen datos de formulario, validarlos y guardarlos en sesión
    # Esto evita la petición extra desde el frontend
    if request.method == 'POST':
        # Los datos pueden venir como JSON (si es fetch) o FormData
        try:
            import json
            if request.content_type == 'application/json':
                post_data = json.loads(request.body)
            else:
                post_data = request.POST
                
            if 'shipping_name' in post_data:
                form = CheckoutForm(post_data)
                if form.is_valid():
                    request.session['checkout_data'] = {
                        'shipping_name': form.cleaned_data['shipping_name'],
                        'shipping_email': form.cleaned_data['shipping_email'],
                        'shipping_phone': form.cleaned_data['shipping_phone'],
                        'shipping_address': form.cleaned_data['shipping_address'],
                        'shipping_city': form.cleaned_data['shipping_city'],
                        'shipping_department': form.cleaned_data.get('shipping_department', ''),
                        'shipping_postal_code': form.cleaned_data.get('shipping_postal_code', ''),
                        'payment_method': 'PAYPAL',
                        'notes': form.cleaned_data.get('notes', ''),
                    }
                else:
                    return JsonResponse({
                        'success': False,
                        'error': 'Formulario inválido',
                        'details': form.errors
                    }, status=400)
        except Exception as e:
            # Si no hay datos de formulario pero sí hay en sesión, continuamos (flujo reintentar)
            if 'checkout_data' not in request.session:
                return JsonResponse({'success': False, 'error': f'Error al procesar datos: {str(e)}'}, status=400)

    # 3. Obtener Token de Acceso de PayPal
    auth = (settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET)
    base_url = "https://api-m.sandbox.paypal.com" if settings.PAYPAL_MODE == "sandbox" else "https://api-m.paypal.com"
    
    try:
        url_token = f"{base_url}/v1/oauth2/token"
        token_res = requests.post(
            url_token, 
            auth=auth, 
            headers={"Accept": "application/json", "Accept-Language": "en_US"}, 
            data={"grant_type": "client_credentials"},
            timeout=10
        ).json()
        access_token = token_res.get('access_token')
        
        if not access_token:
            return JsonResponse({'success': False, 'error': 'Error de autenticación PayPal'}, status=500)
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Error de conexión: {str(e)}'}, status=500)
    
    # 4. Crear la orden en PayPal
    total_amount = str(cart.get_total())
    url_create = f"{base_url}/v2/checkout/orders"
    headers_create = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    order_data = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": "USD",
                "value": total_amount
            },
            "description": f"Compra en MiXiaomiUnlock - {cart.get_total_items()} items"
        }],
        "application_context": {
            "brand_name": "MiXiaomi Unlock",
            "landing_page": "NO_PREFERENCE",
            "user_action": "PAY_NOW",
            "return_url": request.build_absolute_uri('/orders/success/'),
            "cancel_url": request.build_absolute_uri('/orders/cart/')
        }
    }
    
    try:
        response = requests.post(url_create, headers=headers_create, json=order_data, timeout=10)
        response_data = response.json()
        
        if response.status_code == 201:
            return JsonResponse({'success': True, 'order_id': response_data['id']})
        else:
            return JsonResponse({
                'success': False, 
                'error': f"PayPal Error: {response_data.get('message', 'Desconocido')}"
            }, status=response.status_code)
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def capture_paypal_order(request, order_id):
    """
    Captura el pago de una orden de PayPal ya aprobada por el usuario.
    Crea el Order de Django y vincula la Transaction.
    
    Args:
        order_id: ID de la orden de PayPal a capturar
        
    Returns:
        JsonResponse con status de la captura
    """
    from apps.orders.models import Order, OrderItem, Cart
    from django.db import transaction as db_transaction
    
    # 1. Obtener Token de Acceso de PayPal
    auth = (settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET)
    
    # Determinar URL base según el modo
    base_url = "https://api-m.sandbox.paypal.com" if settings.PAYPAL_MODE == "sandbox" else "https://api-m.paypal.com"
    
    url_token = f"{base_url}/v1/oauth2/token"
    headers = {"Accept": "application/json", "Accept-Language": "en_US"}
    data = {"grant_type": "client_credentials"}
    
    try:
        token_res = requests.post(url_token, auth=auth, headers=headers, data=data).json()
        access_token = token_res.get('access_token')
        
        if not access_token:
            return JsonResponse({'status': 'error', 'message': 'Error de autenticación'}, status=500)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    # 2. Capturar la orden en PayPal
    url_capture = f"{base_url}/v2/checkout/orders/{order_id}/capture"
    headers_capture = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.post(url_capture, headers=headers_capture)
        response_data = response.json()
        
        if response_data.get('status') == 'COMPLETED':
            # 3. Obtener datos del formulario desde la sesión
            checkout_data = request.session.get('checkout_data')
            
            if not checkout_data:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Datos de checkout no encontrados en sesión'
                }, status=400)
            
            # 4. Crear Order y Transaction en Django (transacción atómica)
            try:
                with db_transaction.atomic():
                    # Obtener carrito del usuario
                    cart = Cart.objects.get(user=request.user)
                    
                    # Crear Order
                    order = Order.objects.create(
                        user=request.user,
                        shipping_name=checkout_data['shipping_name'],
                        shipping_email=checkout_data['shipping_email'],
                        shipping_phone=checkout_data['shipping_phone'],
                        shipping_address=checkout_data['shipping_address'],
                        shipping_city=checkout_data['shipping_city'],
                        shipping_department=checkout_data.get('shipping_department', ''),
                        shipping_postal_code=checkout_data.get('shipping_postal_code', ''),
                        payment_method=checkout_data.get('payment_method', 'PAYPAL'),
                        payment_status=True,  # Pago confirmado
                        transaction_id=order_id,  # ID de PayPal
                        status=Order.OrderStatus.PENDING,
                        notes=checkout_data.get('notes', '')
                    )
                    
                    # Crear OrderItems desde el carrito
                    cart_items = cart.items.all()
                    for item in cart_items:
                        OrderItem.objects.create(
                            order=order,
                            product=item.product,
                            quantity=item.quantity,
                            price=item.product.price
                        )
                    
                    # Calcular totales del Order
                    order.calculate_totals()
                    
                    # Crear Transaction vinculada al Order
                    amount = response_data['purchase_units'][0]['payments']['captures'][0]['amount']['value']
                    Transaction.objects.create(
                        order_id=order_id,
                        amount=amount,
                        status='COMPLETED'
                    )
                    
                    # Limpiar carrito
                    cart.clear()
                    
                    # Guardar order_id en sesión para la página de éxito
                    request.session['order_id'] = order.id
                    
                    # Limpiar datos de checkout de la sesión
                    if 'checkout_data' in request.session:
                        del request.session['checkout_data']
                    
                    return JsonResponse({
                        'status': 'success',
                        'transaction_id': order_id,
                        'order_id': order.id,
                        'message': 'Pago procesado correctamente'
                    })
                    
            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Error al crear pedido: {str(e)}'
                }, status=500)
                
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'El pago no pudo ser completado'
            }, status=400)
            
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Error al capturar pago: {str(e)}'
        }, status=500)

