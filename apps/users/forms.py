"""
Django-allauth custom forms para MiXiaomiUnlock
Personalización de formularios de registro y login
"""

from allauth.account.forms import SignupForm
from django import forms


class CustomSignupForm(SignupForm):
    """
    Formulario personalizado de registro que añade campos de nombre y apellido
    """
    first_name = forms.CharField(
        max_length=30,
        label='Nombre',
        widget=forms.TextInput(attrs={
            'placeholder': 'Nombre',
            'class': 'w-full px-4 py-4 bg-gray-50 dark:bg-black/20 border-2 border-transparent focus:border-xiaomi rounded-2xl outline-none font-medium dark:text-white placeholder-gray-400'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        label='Apellido',
        widget=forms.TextInput(attrs={
            'placeholder': 'Apellido',
            'class': 'w-full px-4 py-4 bg-gray-50 dark:bg-black/20 border-2 border-transparent focus:border-xiaomi rounded-2xl outline-none font-medium dark:text-white placeholder-gray-400'
        })
    )

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
