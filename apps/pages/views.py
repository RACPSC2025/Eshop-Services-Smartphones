from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from apps.products.models import Product
from apps.orders.models import Order
from .models import Testimonial

# Create your views here.
from apps.products.models import Product, Favorite

# Create your views here.
def home(request):
    # Fetch latest services and products separately
    services = Product.objects.filter(catalog_type=Product.CatalogType.SERVICE).order_by('-id')[:4]
    products = Product.objects.filter(catalog_type=Product.CatalogType.PRODUCT).order_by('-id')[:4]
    
    # Obtener IDs de favoritos del usuario si está autenticado
    user_favorites = []
    if request.user.is_authenticated:
        user_favorites = Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)
    
    return render(request, 'pages/home.html', {
        'products': products,
        'services': services,
        'user_favorites': user_favorites
    })

def contact(request):
    return render(request, 'pages/contact.html')

def about(request):
    return render(request, 'pages/about.html')

@login_required
def submit_testimonial(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id, user=request.user)
        comment = request.POST.get('comment')
        rating = request.POST.get('rating', 5)
        
        Testimonial.objects.create(
            user=request.user,
            order=order,
            comment=comment,
            rating=rating
        )
    return redirect('users:profile')
