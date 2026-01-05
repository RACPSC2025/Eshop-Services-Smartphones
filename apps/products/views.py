from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'products/products.html' # Asegúrate que la ruta sea correcta
    context_object_name = 'product_list'

def get_queryset(self):
        # Agregamos un select_related si tuvieras categorías como modelo, 
        # pero por ahora forzamos la lectura de todos.
        return Product.objects.all().order_by('id')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/details.html'
    context_object_name = 'product'
