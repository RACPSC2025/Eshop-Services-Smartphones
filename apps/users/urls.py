from django.urls import path
from .views import profile, auth, logout_view

app_name = 'users'

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('auth/', auth, name='auth'),
    path('logout/', logout_view, name='logout'),
]