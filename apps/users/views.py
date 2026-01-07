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
                # Find all users with this email (handle duplicates like admin vs regular)
                users_with_email = User.objects.filter(email=email)
                
                if not users_with_email.exists():
                    messages.error(request, "No existe una cuenta con ese correo.")
                    return redirect('users:auth')

                authenticated_user = None
                for u in users_with_email:
                    user = authenticate(request, username=u.username, password=password)
                    if user is not None:
                        authenticated_user = user
                        break
                
                if authenticated_user is not None:
                    # Sync EmailAddress for allauth resilience
                    email_address, created = EmailAddress.objects.get_or_create(
                        user=authenticated_user,
                        email=authenticated_user.email,
                        defaults={'primary': True, 'verified': False}
                    )

                    # Check if email is verified
                    if not email_address.verified and getattr(settings, 'ACCOUNT_EMAIL_VERIFICATION', None) == 'mandatory':
                        login(request, authenticated_user)
                        messages.warning(request, "Tu correo aún no ha sido verificado. Por favor, revisa tu bandeja de entrada.")
                        return redirect('pages:home')
                    else:
                        login(request, authenticated_user)
                        messages.success(request, f"¡Bienvenido de nuevo, {authenticated_user.first_name or authenticated_user.username}!")
                        return redirect('pages:home')
                else:
                    messages.error(request, "Credenciales inválidas. Por favor verifica tu contraseña.")
            except Exception as e:
                messages.error(request, f"Error en el inicio de sesión: {str(e)}")

        # --- REGISTER LOGIC ---
        elif action == 'register':
            email = request.POST.get('email')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')

            # Strict check for existing email to prevent future duplicates
            if User.objects.filter(email=email).exists():
                messages.error(request, "Este correo ya está registrado. Si olvidaste tu contraseña, usa la opción de recuperación.")
                return redirect('users:auth')

            try:
                # Use email as username for new registrations
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )

                # Create EmailAddress for allauth
                email_obj = EmailAddress.objects.create(user=user, email=email, primary=True, verified=False)

                # Trigger verification email (optional based on settings)
                try:
                    email_obj.send_confirmation(request, signup=True)
                except Exception:
                    pass # Email sending might fail in dev without SMTP

                # Auto-login the user after registration
                authenticated_user = authenticate(request, username=email, password=password)
                if authenticated_user is not None:
                    login(request, authenticated_user)
                    messages.success(request, f"¡Cuenta creada exitosamente, {first_name}!")
                    return redirect('pages:home')
                else:
                    messages.info(request, "¡Cuenta creada! Por favor inicia sesión.")
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