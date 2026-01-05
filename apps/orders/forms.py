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
        widgets = {
            'shipping_name': forms.TextInput(attrs={'class': 'w-full rounded-xl border-gray-200 focus:border-xiaomi focus:ring-xiaomi dark:bg-card-dark dark:border-gray-700', 'placeholder': 'Tu nombre completo'}),
            'shipping_email': forms.EmailInput(attrs={'class': 'w-full rounded-xl border-gray-200 focus:border-xiaomi focus:ring-xiaomi dark:bg-card-dark dark:border-gray-700', 'placeholder': 'ejemplo@correo.com'}),
            'shipping_phone': forms.TextInput(attrs={'class': 'w-full rounded-xl border-gray-200 focus:border-xiaomi focus:ring-xiaomi dark:bg-card-dark dark:border-gray-700', 'placeholder': '300 123 4567'}),
            'shipping_address': forms.TextInput(attrs={'class': 'w-full rounded-xl border-gray-200 focus:border-xiaomi focus:ring-xiaomi dark:bg-card-dark dark:border-gray-700', 'placeholder': 'Calle 123 # 45 - 67'}),
            'shipping_city': forms.TextInput(attrs={'class': 'w-full rounded-xl border-gray-200 focus:border-xiaomi focus:ring-xiaomi dark:bg-card-dark dark:border-gray-700'}),
            'shipping_department': forms.TextInput(attrs={'class': 'w-full rounded-xl border-gray-200 focus:border-xiaomi focus:ring-xiaomi dark:bg-card-dark dark:border-gray-700'}),
            'shipping_postal_code': forms.TextInput(attrs={'class': 'w-full rounded-xl border-gray-200 focus:border-xiaomi focus:ring-xiaomi dark:bg-card-dark dark:border-gray-700'}),
            'payment_method': forms.Select(attrs={'class': 'w-full rounded-xl border-gray-200 focus:border-xiaomi focus:ring-xiaomi dark:bg-card-dark dark:border-gray-700'}),
            'notes': forms.Textarea(attrs={'class': 'w-full rounded-xl border-gray-200 focus:border-xiaomi focus:ring-xiaomi dark:bg-card-dark dark:border-gray-700', 'rows': 3, 'placeholder': 'Instrucciones especiales para la entrega...'}),
        }
