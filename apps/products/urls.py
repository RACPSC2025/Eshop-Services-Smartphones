from django.urls import path
from .views import ProductListView, ProductDetailView, toggle_favorite

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('favorite/toggle/<int:product_id>/', toggle_favorite, name='favorite-toggle'),
]
