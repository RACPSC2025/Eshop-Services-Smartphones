from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Favorite



class ProductListView(ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'  # Renaming for consistency with home view
    paginate_by = 12  # Best Practice: Pagination for performance

    def get_queryset(self):
        return Product.objects.all().order_by('-id')  # Newest first

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_favorites = []
        if self.request.user.is_authenticated:
            user_favorites = Favorite.objects.filter(user=self.request.user).values_list('product_id', flat=True)
        context['user_favorites'] = user_favorites
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/details.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_favorites = []
        if self.request.user.is_authenticated:
            user_favorites = Favorite.objects.filter(user=self.request.user).values_list('product_id', flat=True)
        context['user_favorites'] = user_favorites
        return context


@login_required
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        favorite.delete()
        status = 'removed'
    else:
        status = 'added'
        
    return JsonResponse({'status': status})

