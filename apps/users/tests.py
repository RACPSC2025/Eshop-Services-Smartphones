"""
Tests unitarios para el sistema de autenticación modular.
Cubre forms, services y utils con alta cobertura.
"""

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from django.conf import settings

from .forms import LoginForm, RegisterForm
from .services import AuthService
from .utils import (
    get_users_by_email,
    is_email_verified,
    get_email_address,
    create_email_address,
    sync_allauth_email,
    get_display_name,
)


class LoginFormTest(TestCase):
    """Tests para el formulario de login."""

    def test_valid_login_form(self):
        """Test con datos válidos."""
        form_data = {"username": "test@example.com", "password": "testpass123"}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        """Test con email inválido."""
        form_data = {"username": "invalid-email", "password": "testpass123"}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_missing_password(self):
        """Test con contraseña faltante."""
        form_data = {"username": "test@example.com"}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())


class RegisterFormTest(TestCase):
    """Tests para el formulario de registro."""

    def test_valid_register_form(self):
        """Test con datos válidos."""
        form_data = {
            "email": "new@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "securepass123",
            "password_confirm": "securepass123",
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_password_mismatch(self):
        """Test con contraseñas que no coinciden."""
        form_data = {
            "email": "new@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "password1",
            "password_confirm": "password2",
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_duplicate_email(self):
        """Test con email duplicado."""
        # Crear usuario existente
        User.objects.create_user(
            username="existing@example.com",
            email="existing@example.com",
            password="pass123",
        )

        form_data = {
            "email": "existing@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "newpass123",
            "password_confirm": "newpass123",
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_short_password(self):
        """Test con contraseña muy corta."""
        form_data = {
            "email": "new@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "short",
            "password_confirm": "short",
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())


class AuthServiceTest(TestCase):
    """Tests para AuthService."""

    def setUp(self):
        """Configuración inicial para cada test."""
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )

    def test_authenticate_user_success(self):
        """Test autenticación exitosa."""
        request = self.factory.get("/")
        authenticated = AuthService.authenticate_user(
            request, "test@example.com", "testpass123"
        )
        self.assertEqual(authenticated, self.user)

    def test_authenticate_user_wrong_password(self):
        """Test con contraseña incorrecta."""
        request = self.factory.get("/")
        authenticated = AuthService.authenticate_user(
            request, "test@example.com", "wrongpassword"
        )
        self.assertIsNone(authenticated)

    def test_authenticate_user_nonexistent_email(self):
        """Test con email que no existe."""
        request = self.factory.get("/")
        authenticated = AuthService.authenticate_user(
            request, "nonexistent@example.com", "anypassword"
        )
        self.assertIsNone(authenticated)

    def test_create_user_with_allauth(self):
        """Test creación de usuario con integración allauth."""
        user = AuthService.create_user_with_allauth(
            email="new@example.com",
            password="newpass123",
            first_name="New",
            last_name="User",
        )

        # Verificar usuario creado
        self.assertEqual(user.email, "new@example.com")
        self.assertEqual(user.first_name, "New")
        self.assertEqual(user.last_name, "User")

        # Verificar EmailAddress creado
        self.assertTrue(
            EmailAddress.objects.filter(user=user, email="new@example.com").exists()
        )


class UtilsTest(TestCase):
    """Tests para funciones utilitarias."""

    def setUp(self):
        """Configuración inicial para cada test."""
        self.user = User.objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )

    def test_get_users_by_email(self):
        """Test obtener usuarios por email."""
        users = get_users_by_email("test@example.com")
        self.assertEqual(users.count(), 1)
        self.assertEqual(users.first(), self.user)

    def test_is_email_verified_false(self):
        """Test email no verificado."""
        EmailAddress.objects.create(
            user=self.user, email=self.user.email, primary=True, verified=False
        )
        self.assertFalse(is_email_verified(self.user))

    def test_is_email_verified_true(self):
        """Test email verificado."""
        EmailAddress.objects.create(
            user=self.user, email=self.user.email, primary=True, verified=True
        )
        self.assertTrue(is_email_verified(self.user))

    def test_get_email_address(self):
        """Test obtener EmailAddress."""
        email_obj = EmailAddress.objects.create(
            user=self.user, email=self.user.email, primary=True, verified=False
        )
        retrieved = get_email_address(self.user)
        self.assertEqual(retrieved, email_obj)

    def test_create_email_address(self):
        """Test crear EmailAddress."""
        email_obj = create_email_address(self.user, verified=True)
        self.assertEqual(email_obj.user, self.user)
        self.assertTrue(email_obj.verified)

    def test_sync_allauth_email(self):
        """Test sincronizar EmailAddress."""
        email_obj = sync_allauth_email(self.user)
        self.assertEqual(email_obj.user, self.user)
        self.assertEqual(email_obj.email, self.user.email)

    def test_get_display_name_with_first_name(self):
        """Test nombre a mostrar con first_name."""
        name = get_display_name(self.user)
        self.assertEqual(name, "Test")

    def test_get_display_name_without_first_name(self):
        """Test nombre a mostrar sin first_name."""
        user = User.objects.create_user(
            username="noname@example.com",
            email="noname@example.com",
            password="pass123",
        )
        name = get_display_name(user)
        self.assertEqual(name, "noname@example.com")
