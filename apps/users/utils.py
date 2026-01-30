"""
Utilidades compartidas para el sistema de autenticación.
Funciones helper reutilizables en toda la aplicación.
"""

from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from typing import List, Optional


def get_users_by_email(email: str) -> List[User]:
    """
    Obtiene todos los usuarios con un email específico.

    Args:
        email: Email a buscar

    Returns:
        QuerySet de usuarios con ese email
    """
    return User.objects.filter(email=email)


def is_email_verified(user: User) -> bool:
    """
    Verifica si el email del usuario está verificado en Allauth.

    Args:
        user: Usuario a verificar

    Returns:
        True si el email está verificado, False en caso contrario
    """
    try:
        email_address = EmailAddress.objects.get(user=user, email=user.email)
        return email_address.verified
    except EmailAddress.DoesNotExist:
        return False


def get_email_address(user: User) -> Optional[EmailAddress]:
    """
    Obtiene el objeto EmailAddress de allauth para un usuario.

    Args:
        user: Usuario del que obtener el EmailAddress

    Returns:
        EmailAddress object o None si no existe
    """
    try:
        return EmailAddress.objects.get(user=user, email=user.email)
    except EmailAddress.DoesNotExist:
        return None


def create_email_address(user: User, verified: bool = False) -> EmailAddress:
    """
    Crea un EmailAddress para un usuario (para usuarios legacy).

    Args:
        user: Usuario para el que crear EmailAddress
        verified: Si el email debe marcarse como verificado

    Returns:
        EmailAddress creado
    """
    return EmailAddress.objects.create(
        user=user, email=user.email, primary=True, verified=verified
    )


def sync_allauth_email(user: User) -> EmailAddress:
    """
    Sincroniza EmailAddress con Allauth (get_or_create).
    Útil para usuarios creados antes de la integración con Allauth.

    Args:
        user: Usuario a sincronizar

    Returns:
        EmailAddress sincronizado
    """
    email_address, created = EmailAddress.objects.get_or_create(
        user=user, email=user.email, defaults={"primary": True, "verified": False}
    )
    return email_address


def get_display_name(user: User) -> str:
    """
    Obtiene el nombre a mostrar del usuario.
    Prioriza first_name, luego username.

    Args:
        user: Usuario del que obtener el nombre

    Returns:
        Nombre para mostrar
    """
    return user.first_name or user.username
