import tkinter as tk
from tkinter import simpledialog
import ttkbootstrap as ttk
from ttkbootstrap.dialogs.dialogs import Messagebox as messagebox
from ttkbootstrap.constants import *
from database import DatabaseManager
from transactions import PaymentProcessor
import datetime
from PIL import ImageTk, Image
from utils.cart import *

# Constants
CURRENCY = "₦"
CURRENCY_CODE = "USD"
CHECK_PAYMENT_INTERVAL = 10000  # 10 seconds


class CashierInterface(ttk.Frame):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.style = ttk.Style()
        self.user = user
        self.db = DatabaseManager()
        self.payment_processor = PaymentProcessor()
        self.cart = []
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Product Search
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(pady=10)

        ttk.Label(search_frame, text="Search Product:").pack(side=LEFT)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=LEFT, padx=5, expand=True, fill=X)

        search_btn = ttk.Button(
            search_frame, text="Search", command=self.search_product)
        search_btn.pack(side=LEFT)

        # Product List
        self.product_tree = self.create_treeview(main_frame, columns=(
            'id', 'name', 'price', 'stock'), headings=['ID', 'Product Name', 'Price', 'Stock'], height=5)

        # Cart Management
        cart_frame = ttk.Frame(main_frame)
        cart_frame.pack(padx=5)

        ttk.Button(cart_frame, text="Add to Cart",
                   command=self.add_to_cart).pack(side=LEFT, padx=2)
        ttk.Button(cart_frame, text="Update Quantity",
                   command=self.update_quantity).pack(side=LEFT, padx=2)
        ttk.Button(cart_frame, text="Remove Item",
                   command=self.remove_from_cart).pack(side=LEFT, padx=2)
        ttk.Button(cart_frame, text="Clear Cart",
                   command=self.clear_cart).pack(side=LEFT, padx=2)

        self.cart_tree = self.create_treeview(main_frame, columns=(
            'name', 'price', 'qty', 'total'), headings=['Product', 'Unit Price', 'Qty', 'Total'], height=10)

        # Total Display
        total_frame = ttk.Frame(main_frame)
        total_frame.pack(pady=10)

        ttk.Label(total_frame, text="Total:",
                  style='Total.TLabel').pack(padx=5, side=LEFT)
        self.total_label = ttk.Label(
            total_frame, text=f"{CURRENCY}0.00", style='Total.TLabel')
        self.total_label.pack(padx=5, side=LEFT)

        # Payment Buttons
        ttk.Button(total_frame, text="Process Payment",
                   command=self.process_payment).pack(padx=5, side=RIGHT)

    def create_treeview(self, parent, columns, headings, height):
        tree = ttk.Treeview(parent, columns=columns,
                            show='headings', padding=5, height=height,)
        for col, heading in zip(columns, headings):
            tree.heading(col, text=heading)
            tree.column(col, width=150, anchor=CENTER)
        tree.pack(fill=BOTH, pady=10, padx=5)
        return tree

    def search_product(self):
        query = self.search_entry.get()
        if not query:
            self.show_message('Please provide a search parameter',
                              "Required Field", 'warning')
            return
        products = product_search(self.db, query)
        self.product_tree.delete(*self.product_tree.get_children())
        for product in products:
            self.product_tree.insert('', 'end', values=(
                product['id'], product['name'], f"{CURRENCY}{product['price']:.2f}", product['stock']))

    def add_to_cart(self):
        selected = self.product_tree.selection()
        if not selected:
            self.show_message("Please select a product first",
                              "Selection Required", 'warning')
            return

        product_id = self.product_tree.item(selected[0], 'values')[0]

        product = get_product(self.db, product_id=product_id)

        if product['stock'] <= 0:
            self.show_message("This product is out of stock",
                              "Out of Stock", 'error')
            return

        existing = None
        for item in self.cart:
            if item['id'] == product['id']:
                existing = item
                break

        if existing:
            if existing['quantity'] < product['stock']:
                existing['quantity'] += 1
            else:
                self.show_message("Maximum quantity reached",
                                  "Out of Stock", 'error')
        else:
            self.cart.append(
                {'id': product['id'], 'name': product['name'], 'price': product['price'], 'quantity': 1})

        self.update_cart_display()

    def update_quantity(self):
        selected = self.cart_tree.selection()
        if not selected:
            return

        item = self.cart_tree.item(selected[0], 'values')
        product_id = [p['id'] for p in self.cart if p['name'] == item[0]][0]

        new_qty = simpledialog.askinteger(
            "Update Quantity", "Enter new quantity:", minvalue=1)
        if new_qty:
            product = get_product(self.db, product_id)

        if new_qty > product['stock']:
            self.show_message(
                f"Only {product['stock']} available", "Stock Exceeded", 'error')
            return

        for item in self.cart:
            if item['id'] == product_id:
                item['quantity'] = new_qty
                break
        self.update_cart_display()

    def update_cart_display(self):
        self.cart_tree.delete(*self.cart_tree.get_children())
        total = 0

        for item in self.cart:
            item_total = item['price'] * item['quantity']
            total += item_total
            self.cart_tree.insert('', 'end', values=(
                item['name'], f"{CURRENCY}{item['price']:.2f}", item['quantity'], f"{CURRENCY}{item_total:.2f}"))

        self.total_label.config(text=f"{CURRENCY}{total:.2f}")

    def process_payment(self):
        if not self.cart:
            self.show_message(
                "Add items to cart before payment", "Empty Cart", 'warning')
            return
        line_items = []
        for item in self.cart:
            line_items.append({
                "name": item['name'],
                "quantity": str(item['quantity']),
                "base_price_money": {
                    "amount": int(item['price'] * 100),
                    "currency": CURRENCY_CODE
                }
            })

        payment_result = self.payment_processor.create_payment_link(line_items)

        if payment_result["status"] == "error":
            self.show_message(
                payment_result["message"], "Payment Error", 'error')
            return

        payment_url = payment_result["payment_url"]
        order_id = payment_result["order_id"]
        payment_id = payment_result["payment_id"]

        qr_image = self.payment_processor.generate_qr_code(payment_url)
        qr_image_tk = ImageTk.PhotoImage(qr_image)

        payment_window = ttk.Toplevel(self)
        payment_window.title("Scan to Pay")

        qr_label = ttk.Label(payment_window, image=qr_image_tk)
        qr_label.image = qr_image_tk  # Keep a reference to avoid garbage collection
        qr_label.pack(pady=10)

        ttk.Label(payment_window,
                  text="Scan the QR code to complete payment.").pack(pady=5)

        entry = ttk.Entry(payment_window, textvariable=payment_url, width=20)
        entry.insert(0, payment_url)
        entry.pack(pady=5)

        status_label = ttk.Label(
            payment_window, text="Payment Status: Pending")
        status_label.pack(pady=5)

        def check_payment_status():
            verification_result = self.payment_processor.verify_payment(
                order_id=order_id)

            if verification_result["status"] == "success":
                total = sum(item['price'] * item['quantity']
                            for item in self.cart)
                payment_window.destroy()
                self.save_sale("Square Checkout", total, order_id=order_id)
                self.clear_cart()
                self.show_message(
                    "Payment processed successfully.", "Success", 'info')
                return
            elif verification_result["status"] == "pending":
                status_label.config(
                    text=f"Payment Status: {verification_result['state']}")
                self.after(CHECK_PAYMENT_INTERVAL, check_payment_status)
                return
            else:
                status_label.config(text="Payment Status: Failed")
                self.show_message(
                    verification_result["message"], "Payment Failed", 'error')
                return

        def cancel_payment():
            self.payment_processor.delete_payment_link(payment_id)
            payment_window.destroy()
            self.show_message("Payment cancelled", "Cancelled", 'info')

        self.after(CHECK_PAYMENT_INTERVAL, check_payment_status)

        update_status_btn = ttk.Button(
            payment_window, text="Update Status", command=check_payment_status)
        update_status_btn.pack(pady=5)

        cancel_payment_btn = ttk.Button(
            payment_window, text="Cancel Payment", command=cancel_payment, bootstyle="danger")
        cancel_payment_btn.pack(pady=5)

    def clear_cart(self):
        self.cart = []
        self.update_cart_display()

    def remove_from_cart(self):
        selected = self.cart_tree.selection()
        if not selected:
            return

        item_name = self.cart_tree.item(selected[0], 'values')[0]
        self.cart = [item for item in self.cart if item['name'] != item_name]
        self.update_cart_display()

    def save_sale(self, payment_method, total, order_id):
        sale_id = sale_save(self.db, self.user['id'], total, payment_method)

        for item in self.cart:
            try:
                save_saleitem(db=self.db, order_id=order_id, item=item)

                update_productstock(db=self.db, item=item)
            except Exception as e:
                self.show_message(str(e), 'Saving Error', 'error')

    def show_message(self, message, title, msg_type):
        if msg_type == 'warning':
            messagebox.show_warning(title, message)
        elif msg_type == 'error':
            messagebox.show_error(title, message)
        elif msg_type == 'info':
            messagebox.show_info(title, message)
