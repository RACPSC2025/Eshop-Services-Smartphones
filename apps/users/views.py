"""
Vistas de autenticación - Arquitectura modular y minimalista.
Lógica separada en forms, services y utils para mejor mantenibilidad.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from apps.orders.models import Order
from apps.products.models import Favorite
from .services import AuthService
from .utils import get_display_name


def auth(request):
    """
    Vista unificada de autenticación (login y registro).
    Usa arquitectura modular con forms, services y utils separados.
    """
    # Redirigir usuarios ya autenticados
    if request.user.is_authenticated:
        return redirect("users:profile")

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "login":
            return _handle_login(request)
        elif action == "register":
            return _handle_register(request)

    # GET request - mostrar formularios vacíos
    return render(request, "users/auth.html")


def _handle_login(request):
    """
    Maneja el proceso de login usando AuthService.
    Separado en función privada para mejor organización.
    """
    email = request.POST.get("email")
    password = request.POST.get("password")

    # Validar campos requeridos
    if not email or not password:
        messages.error(request, "Por favor completa todos los campos")
        return redirect("users:auth")

    # Autenticar usando el servicio
    user = AuthService.authenticate_user(request, email, password)

    if user:
        # Verificar si email debe estar verificado
        can_login, error_message = AuthService.check_email_verification(user, email)

        if not can_login:
            messages.warning(request, error_message)
            return redirect("users:auth")

        # Login exitoso
        login(request, user)
        display_name = get_display_name(user)
        messages.success(request, f"¡Bienvenido de nuevo, {display_name}!")
        if user.is_staff:
            return redirect("admin:admin_dashboard")
        return redirect("pages:home")
    else:
        messages.error(
            request, "Credenciales inválidas. Por favor verifica tu email y contraseña."
        )
        return redirect("users:auth")


def _handle_register(request):
    """
    Maneja el proceso de registro usando AuthService.
    Crea usuario y EmailAddress, luego auto-login si la verificación no es mandatory.
    """
    email = request.POST.get("email")
    password = request.POST.get("password")
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")

    # Validar campos requeridos
    if not all([email, password, first_name, last_name]):
        messages.error(request, "Todos los campos son requeridos")
        return redirect("users:auth")

    # Validar longitud de contraseña
    if len(password) < 8:
        messages.error(request, "La contraseña debe tener al menos 8 caracteres")
        return redirect("users:auth")

    try:
        # Crear usuario usando el servicio
        user = AuthService.create_user_with_allauth(
            email=email, password=password, first_name=first_name, last_name=last_name
        )

        # Obtener EmailAddress para enviar verificación
        from allauth.account.models import EmailAddress

        email_obj = EmailAddress.objects.get(user=user, email=email)

        # Enviar email de verificación
        verification_sent = AuthService.send_verification_email_on_signup(
            email_obj, request
        )
        email_verification = getattr(settings, "ACCOUNT_EMAIL_VERIFICATION", "optional")

        # Si la verificación es mandatory, no hacer auto-login
        if email_verification == "mandatory" and verification_sent:
            messages.info(
                request,
                f"¡Cuenta creada exitosamente, {first_name}! Por favor verifica tu correo antes de iniciar sesión.",
            )
            return redirect("users:auth")

        # Auto-login si verificación no es mandatory
        login(request, user)
        messages.success(request, f"¡Cuenta creada exitosamente, {first_name}!")
        return redirect("pages:home")

    except Exception as e:
        # Manejo de errores (ej: email duplicado)
        error_message = str(e)
        if "already exists" in error_message or "UNIQUE constraint" in error_message:
            messages.error(
                request,
                "Este correo ya está registrado. Si olvidaste tu contraseña, usa la opción de recuperación.",
            )
        else:
            messages.error(
                request, "Error al crear la cuenta. Por favor intenta de nuevo."
            )

        return redirect("users:auth")


def logout_view(request):
    """Cierra la sesión del usuario"""
    from django.contrib.auth import logout

    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect("pages:home")


@login_required
def profile(request):
    """
    Dashboard del usuario: Info personal, pedidos y favoritos.
    Sin cambios - mantiene funcionalidad original.
    """
    user = request.user
    # Obtener pedidos ordenados por fecha
    orders = Order.objects.filter(user=user).order_by("-created_at")
    # Obtener favoritos
    favorites = Favorite.objects.filter(user=user).select_related("product")

    context = {
        "user": user,
        "orders": orders,
        "favorites": favorites,
        "user_favorites": favorites.values_list("product_id", flat=True),
        "active_tab": "orders",
    }
    return render(request, "users/profile.html", context)
