import json
from django.views import View
from django.views.generic import TemplateView
from django.http import JsonResponse

from django.conf import settings
from django.db import transaction
from django.urls import reverse
from django.shortcuts import get_object_or_404
from apps.orders.models import Cart, Order, OrderItem
from .services import PayPalService


class PaymentView(TemplateView):
    template_name = "payment/paypal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["PAYPAL_CLIENT_ID"] = settings.PAYPAL_CLIENT_ID
        context["amount"] = self.request.GET.get("amount", "10.00")
        return context


class CreatePayPalOrderView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            # In a real scenario, you usually calculate amount on backend based on cart items
            # Here we take amount from frontend for reusability demonstration, but validate carefully in production
            amount = data.get("amount", "10.00")
            currency = data.get("currency", "USD")

            service = PayPalService()
            order = service.create_order(amount, currency)

            if order and "id" in order:
                return JsonResponse(order)
            else:
                return JsonResponse(
                    {"error": "Failed to create PayPal order"}, status=500
                )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class CapturePayPalOrderView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "User must be logged in"}, status=403)

        try:
            data = json.loads(request.body)
            order_id = data.get("orderID")

            service = PayPalService()
            capture = service.capture_order(order_id)

            if capture and (
                capture.get("status") == "COMPLETED" or "purchase_units" in capture
            ):
                # Payment successful, now create the internal order
                with transaction.atomic():
                    # 1. Get User Cart
                    cart = get_object_or_404(Cart, user=request.user)
                    if cart.get_total_items() == 0:
                        return JsonResponse({"error": "Cart is empty"}, status=400)

                    # 2. Prepare Order Data (Use Profile or Defaults)
                    shipping_data = {
                        "shipping_name": f"{request.user.first_name} {request.user.last_name}",
                        "shipping_email": request.user.email,
                        "shipping_phone": "",
                        "shipping_address": "",
                        "shipping_city": "",
                        "shipping_department": "",
                        "shipping_postal_code": "",
                    }

                    if hasattr(request.user, "profile"):
                        profile = request.user.profile
                        shipping_data.update(
                            {
                                "shipping_phone": getattr(profile, "phone", ""),
                                "shipping_address": getattr(profile, "address", ""),
                                "shipping_city": getattr(profile, "city", ""),
                                "shipping_department": getattr(
                                    profile, "department", ""
                                ),
                                "shipping_postal_code": getattr(
                                    profile, "postal_code", ""
                                ),
                            }
                        )

                    # 3. Create Order
                    order = Order.objects.create(
                        user=request.user,
                        payment_method=Order.PaymentMethod.PAYPAL,
                        payment_status=True,
                        transaction_id=capture.get("id"),  # PayPal Transaction ID
                        status=Order.OrderStatus.PROCESSING,
                        **shipping_data,
                    )

                    # 4. Move Cart Items to Order Items
                    cart_items = cart.items.all()
                    for item in cart_items:
                        OrderItem.objects.create(
                            order=order,
                            product=item.product,
                            quantity=item.quantity,
                            price=item.product.price,
                        )

                    # 5. Calculate Totals
                    order.calculate_totals()

                    # 6. Clear Cart
                    cart.clear()

                    # 7. Set Session
                    request.session["order_id"] = order.id

                return JsonResponse(
                    {
                        "status": "COMPLETED",
                        "details": capture,
                        "redirect_url": reverse("orders:order_success"),
                    }
                )
            else:
                # It might return error details provided by PayPal Service
                return JsonResponse(
                    capture if capture else {"error": "Failed to capture order"},
                    status=500,
                )

        except Exception as e:
            import traceback

            traceback.print_exc()
            return JsonResponse({"error": str(e)}, status=500)
