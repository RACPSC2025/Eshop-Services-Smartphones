import requests

from django.conf import settings


class PayPalService:
    def __init__(self):
        self.client_id = settings.PAYPAL_CLIENT_ID
        self.secret = settings.PAYPAL_SECRET
        if settings.DEBUG:
            self.base_url = "https://api-m.sandbox.paypal.com"
        else:
            self.base_url = "https://api-m.paypal.com"

    def get_access_token(self):
        url = f"{self.base_url}/v1/oauth2/token"
        headers = {
            "Accept": "application/json",
            "Accept-Language": "en_US",
        }
        data = {"grant_type": "client_credentials"}

        try:
            response = requests.post(
                url, headers=headers, data=data, auth=(self.client_id, self.secret)
            )
            response.raise_for_status()
            return response.json()["access_token"]
        except Exception as e:
            print(f"Error getting PayPal access token: {e}")
            return None

    def create_order(self, amount, currency="USD"):
        access_token = self.get_access_token()
        if not access_token:
            return None

        url = f"{self.base_url}/v2/checkout/orders"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        payload = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": currency,
                        "value": str(amount),
                    }
                }
            ],
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error creating PayPal order: {e}")
            return None

    def capture_order(self, order_id):
        access_token = self.get_access_token()
        if not access_token:
            return None

        url = f"{self.base_url}/v2/checkout/orders/{order_id}/capture"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        try:
            response = requests.post(url, headers=headers)
            # 422 Unprocessable Entity can happen if already captured, handle gracefully if needed
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error capturing PayPal order: {e}")
            # Return error response content if available for debugging
            if hasattr(e, "response") and e.response is not None:
                return e.response.json()
            return None
