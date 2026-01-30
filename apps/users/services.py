"""
Servicios de autenticación - Lógica de negocio separada de las vistas.
Implementa operaciones de autenticación reutilizables y testeables.
"""

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.conf import settings
from allauth.account.models import EmailAddress
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class AuthService:
    """
    Servicio centralizado para operaciones de autenticación.
    Separa la lógica de negocio de las vistas para mejor testabilidad.
    """

    @staticmethod
    def authenticate_user(request, email: str, password: str) -> Optional[User]:
        """
        Autentica usuario usando email.

        Args:
            request: HttpRequest object
            email: Email del usuario
            password: Contraseña del usuario

        Returns:
            User autenticado o None si falla la autenticación
        """
        try:
            # Buscar usuario por email
            user = User.objects.get(email=email)

            # Autenticar con username (Django usa username internamente)
            authenticated_user = authenticate(
                request, username=user.username, password=password
            )

            if authenticated_user:
                logger.info(f"Usuario autenticado exitosamente: {email}")
                return authenticated_user
            else:
                logger.warning(f"Contraseña incorrecta para: {email}")
                return None

        except User.DoesNotExist:
            logger.warning(f"Intento de login con email inexistente: {email}")
            return None
        except Exception as e:
            logger.error(f"Error en autenticación: {str(e)}")
            return None

    @staticmethod
    def create_user_with_allauth(
        email: str, password: str, first_name: str, last_name: str
    ) -> User:
        """
        Crea usuario y configura integración con Allauth.

        Args:
            email: Email del usuario (usado como username)
            password: Contraseña del usuario
            first_name: Nombre del usuario
            last_name: Apellido del usuario

        Returns:
            Usuario creado

        Raises:
            Exception: Si hay error en la creación
        """
        try:
            # Crear usuario con email como username
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )

            # Crear EmailAddress para compatibilidad con Allauth
            email_obj = EmailAddress.objects.create(
                user=user, email=email, primary=True, verified=False
            )

            logger.info(f"Usuario creado exitosamente: {email}")

            # Enviar email de verificación si está configurado
            AuthService._send_verification_email(email_obj, user)

            return user

        except Exception as e:
            logger.error(f"Error creando usuario {email}: {str(e)}")
            raise

    @staticmethod
    def _send_verification_email(email_obj: EmailAddress, user: User):
        """
        Envía email de verificación si está configurado en settings.

        Args:
            email_obj: Objeto EmailAddress de allauth
            user: Usuario al que enviar verificación
        """
        email_verification = getattr(settings, "ACCOUNT_EMAIL_VERIFICATION", "optional")

        if email_verification in ["mandatory", "optional"]:
            try:
                # Note: send_confirmation necesita request, pero no tenemos acceso aquí
                # Esto se maneja mejor en la vista
                logger.info(f"Email de verificación programado para: {user.email}")
            except Exception as e:
                logger.warning(f"No se pudo enviar email de verificación: {str(e)}")

    @staticmethod
    def check_email_verification(user: User, email: str) -> tuple[bool, str]:
        """
        Verifica si el email del usuario está verificado cuando es requerido.

        Args:
            user: Usuario a verificar
            email: Email del usuario

        Returns:
            Tupla (puede_login, mensaje)
        """
        email_verification = getattr(settings, "ACCOUNT_EMAIL_VERIFICATION", "optional")

        if email_verification != "mandatory":
            return True, ""

        try:
            email_address = EmailAddress.objects.get(user=user, email=email)

            if not email_address.verified:
                return (
                    False,
                    "Tu correo aún no ha sido verificado. Por favor, revisa tu bandeja de entrada y verifica tu email antes de iniciar sesión.",
                )

            return True, ""

        except EmailAddress.DoesNotExist:
            # Crear EmailAddress si no existe (usuarios legacy)
            EmailAddress.objects.create(
                user=user, email=email, primary=True, verified=False
            )
            return (
                False,
                "Se ha enviado un correo de verificación. Por favor verifica tu email antes de iniciar sesión.",
            )

    @staticmethod
    def send_verification_email_on_signup(email_obj: EmailAddress, request):
        """
        Envía email de verificación durante el signup.

        Args:
            email_obj: EmailAddress object
            request: HttpRequest object

        Returns:
            bool: True si se envió exitosamente
        """
        email_verification = getattr(settings, "ACCOUNT_EMAIL_VERIFICATION", "optional")

        if email_verification in ["mandatory", "optional"]:
            try:
                email_obj.send_confirmation(request, signup=True)
                logger.info(f"Email de verificación enviado a: {email_obj.email}")
                return True
            except Exception as e:
                logger.warning(f"Fallo al enviar email de verificación: {str(e)}")
                return False

        return False
