from .models import Cart

def cart_context(request):
    """
    Context processor para hacer disponible la información del carrito en todos los templates.
    Retorna siempre variables iterables/seguras para evitar VariableDoesNotExist.
    """
    cart = None
    cart_count = 0
    cart_total = 0
    cart_items = []  # Siempre iterable, nunca None
    
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        elif request.session.session_key:
            cart = Cart.objects.filter(session_key=request.session.session_key).first()
        
        if cart:
            cart_count = cart.get_total_items()
            cart_total = cart.get_total()
            cart_items = list(cart.items.select_related('product').all())
    except Exception:
        pass

    
    return {
        'cart': cart,
        'cart_count': cart_count,
        'cart_total': cart_total,
        'cart_items': cart_items,
    }
