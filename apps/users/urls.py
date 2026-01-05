from django.urls import path, include
from .views import profile, auth

app_name = 'users'

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('auth/', auth, name='auth'),
]