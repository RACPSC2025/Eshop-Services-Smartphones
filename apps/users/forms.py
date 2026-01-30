"""
Django Forms para autenticación con validación robusta.
Reemplaza validación manual con validadores automáticos de Django.
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError


class LoginForm(AuthenticationForm):
    """
    Formulario de login que acepta email en lugar de username.
    Hereda de AuthenticationForm para compatibilidad con Django Auth.
    """

    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "usuario@ejemplo.com",
                "class": "w-full pl-12 pr-4 py-4 bg-gray-50 dark:bg-black/20 border-2 border-transparent focus:border-xiaomi rounded-2xl outline-none transition-all font-medium text-gray-900 dark:text-white placeholder-gray-400",
            }
        ),
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "••••••••",
                "class": "w-full pl-12 pr-4 py-4 bg-gray-50 dark:bg-black/20 border-2 border-transparent focus:border-xiaomi rounded-2xl outline-none transition-all font-medium text-gray-900 dark:text-white placeholder-gray-400",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove auto_id to avoid duplicate IDs in template
        self.auto_id = False


class RegisterForm(forms.ModelForm):
    """
    Formulario de registro con validaciones automáticas.
    Valida email único, contraseñas coincidentes y campos requeridos.
    """

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Crea una contraseña",
                "class": "w-full px-4 py-4 bg-gray-50 dark:bg-black/20 border-2 border-transparent focus:border-xiaomi rounded-2xl outline-none font-medium dark:text-white",
            }
        ),
    )
    password_confirm = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirma tu contraseña",
                "class": "w-full px-4 py-4 bg-gray-50 dark:bg-black/20 border-2 border-transparent focus:border-xiaomi rounded-2xl outline-none font-medium dark:text-white",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "tu@email.com",
                    "class": "w-full px-4 py-4 bg-gray-50 dark:bg-black/20 border-2 border-transparent focus:border-xiaomi rounded-2xl outline-none font-medium dark:text-white",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": "Nombre",
                    "class": "w-full px-4 py-4 bg-gray-50 dark:bg-black/20 border-2 border-transparent focus:border-xiaomi rounded-2xl outline-none font-medium dark:text-white",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "placeholder": "Apellido",
                    "class": "w-full px-4 py-4 bg-gray-50 dark:bg-black/20 border-2 border-transparent focus:border-xiaomi rounded-2xl outline-none font-medium dark:text-white",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields required
        for field_name in self.fields:
            self.fields[field_name].required = True

    def clean(self):
        """Valida que las contraseñas coincidan."""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Las contraseñas no coinciden")

        return cleaned_data

    def clean_email(self):
        """Valida que el email sea único en el sistema."""
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email=email).exists():
            raise ValidationError(
                "Este correo ya está registrado. Si olvidaste tu contraseña, usa la opción de recuperación."
            )
        return email

    def clean_password(self):
        """Valida la fortaleza de la contraseña."""
        password = self.cleaned_data.get("password")
        if password and len(password) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres")
        return password
