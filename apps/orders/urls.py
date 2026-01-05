from django.urls import path, include
from .views import cart, checkout

app_name = 'orders'

urlpatterns = [
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
]

