from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'shipping_name', 'shipping_email', 'shipping_phone',
            'shipping_address', 'shipping_city', 'shipping_department',
            'shipping_postal_code', 'payment_method', 'notes'
        ]
        input_classes = (
            'w-full py-2.5 px-4 rounded-xl border-2 border-gray-100 dark:border-gray-800 '
            'bg-gray-50/50 dark:bg-black/20 text-gray-900 dark:text-white '
            'placeholder:text-gray-400 focus:border-xiaomi focus:ring-4 focus:ring-xiaomi/10 '
            'transition-all duration-300 outline-none'
        )
        widgets = {
            'shipping_name': forms.TextInput(attrs={'class': input_classes, 'placeholder': 'Ej: Juan Pérez'}),
            'shipping_email': forms.EmailInput(attrs={'class': input_classes, 'placeholder': 'tu@email.com'}),
            'shipping_phone': forms.TextInput(attrs={'class': input_classes, 'placeholder': 'Ej: 300 123 4567'}),
            'shipping_address': forms.TextInput(attrs={'class': input_classes, 'placeholder': 'Dirección completa'}),
            'shipping_city': forms.TextInput(attrs={'class': input_classes, 'placeholder': 'Tu ciudad'}),
            'shipping_department': forms.TextInput(attrs={'class': input_classes, 'placeholder': 'Departamento'}),
            'shipping_postal_code': forms.TextInput(attrs={'class': input_classes, 'placeholder': 'Opcional'}),
            'payment_method': forms.Select(attrs={'class': input_classes}),
            'notes': forms.Textarea(attrs={'class': input_classes, 'rows': 3, 'placeholder': 'Ej: Entregar en portería...'}),
        }
