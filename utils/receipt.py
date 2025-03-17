from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import datetime
import os
CURRENCY = "₦"
# CURRENCY_CODE = "USD"
# CHECK_PAYMENT_INTERVAL = 10000  # 10 seconds


def generate_receipt(user, cart):
    pdf = canvas.Canvas(
        # 'testrecep/' + f"receipt_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
        "/testrecep", pagesize=letter)
    pdf.setLineWidth(1)
    pdf.setFont("Helvetica", 12)

    pdf.drawString(100, 750, "Supermarket POS Receipt")
    pdf.drawString(
        100, 730, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    pdf.drawString(100, 710, f"Cashier: {user['username']}")

    pdf.drawString(100, 680, "Items:")
    y = 660
    for item in cart:
        pdf.drawString(120, y, f"{item['name']} x{item['quantity']}")
        y -= 20

    pdf.drawString(
        100, y, f"Total: {CURRENCY}{sum(item['price'] * item['quantity'] for item in cart):.2f}")
    return pdf
