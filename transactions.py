import requests


class PaymentProcessor:
    def __init__(self):
        self.test_mode = True
        self.flutterwave_test_key = "FLWSECK_TEST-xxxxxxxxxxxx"  # Replace with test key

    def process_payment(self, amount, method, card_details=None):
        if method == "cash":
            return {"status": "success", "change": amount}

        elif method == "card":
            if self.test_mode:
                return self.mock_flutterwave_payment(amount, card_details)
            else:
                return self.real_flutterwave_payment(amount, card_details)

    def mock_flutterwave_payment(self, amount, card):
        # Test card numbers: 5531886652142950, 4556052704172643
        test_response = {
            "status": "success",
            "message": "Payment approved",
            "transaction_id": "TEST1234",
            "amount": amount
        }
        return test_response

    def real_flutterwave_payment(self, amount, card):
        headers = {
            "Authorization": f"Bearer {self.flutterwave_test_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "card_number": card['number'],
            "cvv": card['cvv'],
            "expiry_month": card['exp_month'],
            "expiry_year": card['exp_year'],
            "currency": "NGN",
            "amount": str(amount),
            "email": "customer@example.com",
            "tx_ref": "POS-"+datetime.now().strftime("%Y%m%d%H%M%S")
        }

        try:
            response = requests.post(
                "https://api.flutterwave.com/v3/charges?type=card",
                json=payload,
                headers=headers
            )
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}
