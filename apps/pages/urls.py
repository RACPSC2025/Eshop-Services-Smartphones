from django.urls import path
from .views import home, contact, about, submit_testimonial

app_name = 'pages'

urlpatterns = [
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('testimonial/submit/<int:order_id>/', submit_testimonial, name='testimonial-submit'),
]