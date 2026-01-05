from django.urls import path
from .views import home, contact, about

app_name = 'pages'

urlpatterns = [
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
]