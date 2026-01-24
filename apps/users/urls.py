from django.urls import path
from .views import profile

app_name = 'users'

urlpatterns = [
    path('profile/', profile, name='profile'),
    # auth y logout ahora usan allauth:
    # /accounts/login/, /accounts/signup/, /accounts/logout/
]