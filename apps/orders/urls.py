from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Vistas HTML
    path('cart/', views.cart_view, name='cart_view'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/', views.order_success, name='order_success'),

    
    # API Endpoints (AJAX)
    path('api/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('api/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('api/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
]
