from square.http.auth.o_auth_2 import BearerAuthCredentials
from square.client import Client
import uuid
import time
import os
import qrcode
from io import BytesIO
from PIL import ImageTk, Image
from typing import List, Dict, Any, Union


class PaymentProcessor:
    def __init__(self):
        # Initialize the Square client with BearerAuthCredentials
        self.client = Client(
            bearer_auth_credentials=BearerAuthCredentials(
                access_token=os.environ['SQUARE_ACCESS_TOKEN']
            ),
            environment='sandbox'
        )
        # Get the location ID from environment variables
        self.location_id = os.getenv('SQUARE_LOCATION_ID')

    def create_payment_link(self, line_items: List[Dict[str, Any]]):
        """
        Create a payment link for the given line items.
        """
        # Prepare the checkout request
        body = {
            "order": {
                "location_id": self.location_id,
                "line_items": line_items
            },
            "checkout_options": {
                "accepted_payment_methods": {
                    "google_pay": True
                }
            }
        }

        try:
            # Create the payment link
            result = self.client.checkout.create_payment_link(body=body)
            if result.is_success():
                return {
                    "status": "success",
                    "payment_id": result.body['payment_link']['id'],
                    "payment_url": result.body['payment_link']['url'],
                    "order_id": result.body['payment_link']['order_id']
                }
            elif result.is_error():
                return {
                    "status": "error",
                    "message": result.errors[0]['detail']
                }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def generate_qr_code(self, payment_url: str):
        """
        Generate a QR code for the given payment URL.
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(payment_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        return img

    def verify_payment(self, order_id: str):
        """
        Verify the payment status for the given order ID.
        """
        try:
            # Retrieve the order details
            result = self.client.orders.retrieve_order(order_id)

            if result.is_success():
                order = result.body['order']
                if order['state'] == "OPEN":
                    return {"status": "success", "order": order, }
                else:
                    return {"status": "pending", "message": "Payment not yet completed", 'state': order['state']}
            elif result.is_error():
                return {
                    "status": "error",
                    "message": result.errors[0]['detail']
                }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def delete_payment_link(self, payment_id: str):
        """
        Delete the payment link for the given order ID.
        """
        try:
            # Delete the payment link
            result = self.client.checkout.delete_payment_link(payment_id)
            if result.is_success():
                return {"status": "success"}
            elif result.is_error():
                return {
                    "status": "error",
                    "message": result.errors[0]['detail']
                }
        except Exception as e:
            return {"status": "error", "message": str(e)}
