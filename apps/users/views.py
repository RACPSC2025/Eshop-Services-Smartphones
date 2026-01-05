from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from apps.orders.models import Order
from allauth.account.models import EmailAddress

def auth(request):
    """Maneja el inicio de sesión y registro de usuarios con Allauth Integration"""
    if request.user.is_authenticated:
        return redirect('users:profile')

    if request.method == 'POST':
        action = request.POST.get('action')
        
        # --- LOGIN LOGIC ---
        if action == 'login':
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(request, username=user_obj.username, password=password)
                
                if user is not None:
                    # Sync EmailAddress for allauth resilience
                    email_address, created = EmailAddress.objects.get_or_create(
                        user=user, 
                        email=user.email,
                        defaults={'primary': True, 'verified': False}
                    )

                    # Check if email is verified
                    if not email_address.verified and getattr(settings, 'ACCOUNT_EMAIL_VERIFICATION', None) == 'mandatory':
                        messages.warning(request, "Tu correo aún no ha sido verificado. Por favor, revisa tu bandeja de entrada.")
                        return redirect('users:auth')
                        
                    login(request, user)
                    messages.success(request, f"¡Bienvenido de nuevo, {user.first_name}!")
                    return redirect('pages:home')
                else:
                    messages.error(request, "Credenciales inválidas.")
            except User.DoesNotExist:
                messages.error(request, "No existe una cuenta con ese correo.")

        # --- REGISTER LOGIC ---
        elif action == 'register':
            email = request.POST.get('email')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            
            if User.objects.filter(email=email).exists():
                messages.error(request, "Este correo ya está registrado.")
                return redirect('users:auth')

            try:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                
                # Create EmailAddress for allauth
                email_obj = EmailAddress.objects.create(user=user, email=email, primary=True, verified=False)
                
                # Trigger verification email
                email_obj.send_confirmation(request, signup=True)
                
                messages.info(request, "¡Cuenta creada! Hemos enviado un correo de verificación. Por favor, confírmalo para poder comprar.")
                return redirect('users:auth')

            except Exception as e:
                messages.error(request, f"Error en el registro: {str(e)}")

    return render(request, 'users/auth.html')

def logout_view(request):
    """Cierra la sesión del usuario"""
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('pages:home')

from apps.products.models import Favorite

@login_required
def profile(request):
    """Dashboard del usuario: Info personal, pedidos y favoritos"""
    user = request.user
    # Obtener pedidos ordenados por fecha
    orders = Order.objects.filter(user=user).order_by('-created_at')
    # Obtener favoritos
    favorites = Favorite.objects.filter(user=user).select_related('product')
    
    context = {
        'user': user,
        'orders': orders,
        'favorites': favorites,
        'user_favorites': favorites.values_list('product_id', flat=True),
        'active_tab': 'orders'
    }
    return render(request, 'users/profile.html', context)