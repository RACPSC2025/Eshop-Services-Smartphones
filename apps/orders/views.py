from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.contrib import messages
from django.db import transaction
from apps.products.models import Product
from .models import Cart, CartItem, Order, OrderItem
from .forms import CheckoutForm


def _get_cart(request):
    """Helper para obtener o crear el carrito basado en sesión o usuario"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        
        cart, created = Cart.objects.get_or_create(
            session_key=request.session.session_key,
            defaults={'user': None}
        )
    return cart


def _get_cart_context(cart):
    """Helper para generar contexto consistente del carrito"""
    cart_items = list(cart.items.select_related('product').all().order_by('id'))
    return {

        'cart': cart,
        'cart_items': cart_items,
        'cart_count': cart.get_total_items(),
        'cart_total': cart.get_total(),
    }


@require_POST
def add_to_cart(request, product_id):
    """API Endpoint para agregar al carrito vía AJAX."""
    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'error': 'login_required',
            'message': 'Debes iniciar sesión para comprar.'
        }, status=403)

    cart = _get_cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 0}
    )
    cart_item.increase_quantity()
    
    # Contexto actualizado
    ctx = _get_cart_context(cart)
    mini_cart_html = render_to_string('components/mini_cart.html', ctx, request=request)
    
    return JsonResponse({
        'success': True,
        'cart_count': ctx['cart_count'],
        'mini_cart_html': mini_cart_html,
        'message': f'{product.name} agregado al carrito'
    })


@require_POST
def remove_from_cart(request, item_id):
    """API Endpoint para eliminar item"""
    cart = _get_cart(request)
    try:
        item = CartItem.objects.get(id=item_id, cart=cart)
        item.delete()
        
        ctx = _get_cart_context(cart)
        mini_cart_html = render_to_string('components/mini_cart.html', ctx, request=request)
        
        try:
            cart_html = render_to_string('orders/partials/cart_table.html', ctx, request=request)
        except:
            cart_html = None
        
        return JsonResponse({
            'success': True,
            'cart_count': ctx['cart_count'],
            'cart_total': float(ctx['cart_total']),
            'mini_cart_html': mini_cart_html,
            'cart_html': cart_html,
            'message': 'Producto eliminado'
        })
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Item no encontrado'}, status=404)


@require_POST
def update_cart_item(request, item_id):
    """API Endpoint para actualizar la cantidad (+/-)"""
    cart = _get_cart(request)
    action = request.POST.get('action')
    
    try:
        item = CartItem.objects.get(id=item_id, cart=cart)
        
        if action == 'increase':
            item.increase_quantity()
        elif action == 'decrease':
            item.decrease_quantity()
        
        # Verificar si el item aún existe
        try:
            item.refresh_from_db()
            item_total = float(item.get_total_price())
        except CartItem.DoesNotExist:
            item_total = 0

        ctx = _get_cart_context(cart)
        mini_cart_html = render_to_string('components/mini_cart.html', ctx, request=request)
        
        try:
            cart_html = render_to_string('orders/partials/cart_table.html', ctx, request=request)
        except:
            cart_html = None

        return JsonResponse({
            'success': True,
            'cart_count': ctx['cart_count'],
            'item_total': item_total,
            'cart_subtotal': float(cart.get_subtotal()),
            'cart_tax': float(cart.get_tax()),
            'cart_total': float(ctx['cart_total']),
            'mini_cart_html': mini_cart_html,
            'cart_html': cart_html
        })
        
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False}, status=404)


def cart_view(request):
    """Vista principal del carrito de compras"""
    cart = _get_cart(request)
    ctx = _get_cart_context(cart)
    return render(request, 'orders/cart.html', ctx)


@login_required
def checkout(request):
    """Vista de Checkout: Procesa el pedido"""
    cart = _get_cart(request)
    
    if cart.get_total_items() == 0:
        messages.warning(request, "Tu carrito está vacío.")
        return redirect('orders:cart_view')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    order = form.save(commit=False)
                    if request.user.is_authenticated:
                        order.user = request.user
                    order.status = Order.OrderStatus.PENDING
                    order.save()
                    
                    cart_items = cart.items.all()
                    for item in cart_items:
                        OrderItem.objects.create(

                            order=order,
                            product=item.product,
                            quantity=item.quantity,
                            price=item.product.price
                        )
                    
                    order.calculate_totals()
                    cart.clear()
                    
                    request.session['order_id'] = order.id
                    return redirect('orders:order_success')
                    
            except Exception as e:
                messages.error(request, f"Error al procesar el pedido: {str(e)}")
    else:
        initial_data = {}
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            profile = request.user.profile
            initial_data = {
                'shipping_phone': profile.phone,
                'shipping_address': profile.address,
                'shipping_city': profile.city,
                'shipping_department': profile.department,
                'shipping_postal_code': profile.postal_code,
            }
        form = CheckoutForm(initial=initial_data)
    
    ctx = _get_cart_context(cart)
    ctx['form'] = form
    return render(request, 'orders/checkout.html', ctx)


def order_success(request):
    """Vista de confirmación de compra"""
    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('pages:home')
        
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return redirect('pages:home')
        
    return render(request, 'orders/success.html', {'order': order})
