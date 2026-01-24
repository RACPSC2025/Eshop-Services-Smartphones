from django.urls import path
from . import views

urlpatterns = [
    path("", views.PaymentView.as_view(), name="payment_index"),
    path(
        "create-order/",
        views.CreatePayPalOrderView.as_view(),
        name="payment_create_order",
    ),
    path(
        "capture-order/",
        views.CapturePayPalOrderView.as_view(),
        name="payment_capture_order",
    ),
]
