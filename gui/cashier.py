import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import ttkbootstrap as ttk
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.constants import *
from database import DatabaseManager
from transactions import PaymentProcessor
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import datetime


class CashierInterface(ttk.Frame):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user
        self.db = DatabaseManager()
        self.cart = []
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        # Left Panel - Product Search and Cart
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # Product Search
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(pady=5)

        ttk.Label(search_frame, text="Search Product:").pack(side=LEFT)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=LEFT, padx=5, expand=True, fill=X)

        search_btn = ttk.Button(
            search_frame, text="Search", command=self.search_product)
        search_btn.pack(side=LEFT)

        # Product List
        self.product_tree = ttk.Treeview(left_frame, columns=(
            'id', 'name', 'price', 'stock'), show='headings', padding=5, height=5)
        self.product_tree.heading('id', text='ID')
        self.product_tree.heading('name', text='Product Name')
        self.product_tree.heading('price', text='Price')
        self.product_tree.heading('stock', text='Stock')
        self.product_tree.pack(expand=False, pady=5, padx=5)

        # Cart Management
        cart_frame = ttk.Frame(left_frame)
        cart_frame.pack(padx=5,)

        ttk.Button(cart_frame, text="Add to Cart",
                   command=self.add_to_cart).pack(side=LEFT, padx=2)
        ttk.Button(cart_frame, text="Update Quantity",
                   command=self.update_quantity).pack(side=LEFT, padx=2)
        ttk.Button(cart_frame, text="Remove Item",
                   command=self.remove_from_cart).pack(side=LEFT, padx=2)
        ttk.Button(cart_frame, text="Clear Cart",
                   command=self.clear_cart).pack(side=LEFT, padx=2)

        # Right Panel - Cart Display
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=RIGHT, fill=BOTH)

        self.cart_tree = ttk.Treeview(left_frame, columns=(
            'name', 'price', 'qty', 'total'), show='headings', height=10)
        self.cart_tree.heading('name', text='Product')
        self.cart_tree.heading('price', text='Unit Price')
        self.cart_tree.heading('qty', text='Qty')
        self.cart_tree.heading('total', text='Total')
        self.cart_tree.pack(fill=BOTH, expand=True, padx=10, pady=5)

        # Total Display
        total_frame = ttk.Frame(left_frame)
        total_frame.pack(fill=X, pady=5)

        ttk.Label(total_frame, text="Total:",
                  style='Total.TLabel').pack(padx=5)
        self.total_label = ttk.Label(
            total_frame, text="₦0.00", style='Total.TLabel')
        self.total_label.pack(padx=5)

        # Payment Buttons
        ttk.Button(total_frame, text="Process Payment",
                   command=self.process_payment).pack(padx=5)

    def search_product(self):
        query = self.search_entry.get()
        if not query or (query == ''):
            message_box = Messagebox()
            message_box.show_warning(
                message='Please provide a search parameter', title="Required Fieldd ", parent=self, alert=True, )
            return
        products = self.db.execute_query(
            "SELECT * FROM Products WHERE name LIKE ? OR id = ?",
            (f"%{query}%", query),
            fetch=True
        )

        self.product_tree.delete(*self.product_tree.get_children())
        index = len(products)//2
        for product in products:
            id = self.product_tree.insert('', 'end', values=(
                product['id'],
                product['name'],
                f"₦{product['price']:.2f}",
                product['stock']
            ))

    def add_to_cart(self):
        selected = self.product_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required",
                                   "Please select a product first")
            return

        product_id = self.product_tree.item(selected[0], 'values')[0]
        product = self.db.execute_query(
            "SELECT * FROM Products WHERE id = ?",
            (product_id,),
            fetch=True
        )[0]

        # Check stock
        if product['stock'] <= 0:
            messagebox.showerror(
                "Out of Stock", "This product is out of stock")
            return

        # Add to cart or update quantity
        existing = next(
            (item for item in self.cart if item['id'] == product_id), None)
        if existing:
            if existing['quantity'] < product['stock']:
                existing['quantity'] += 1
            else:
                messagebox.showerror(
                    "Out of Stock", "Maximum quantity reached")
        else:
            self.cart.append({
                'id': product_id,
                'name': product['name'],
                'price': product['price'],
                'quantity': 1
            })

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
            product = self.db.execute_query(
                "SELECT stock FROM Products WHERE id = ?",
                (product_id,),
                fetch=True
            )[0]

        if new_qty > product['stock']:
            messagebox.showerror(
                "Stock Exceeded", f"Only {product['stock']} available")
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
                item['name'],
                f"₦{item['price']:.2f}",
                item['quantity'],
                f"₦{item_total:.2f}"
            ))

        self.total_label.config(text=f"₦{total:.2f}")

    def process_payment(self):
        if not self.cart:
            messagebox.showwarning(
                "Empty Cart", "Add items to cart before payment")
            return

        payment_window = ttk.Toplevel(self)
        payment_window.title("Payment Processing")

        # Payment method selection
        ttk.Label(payment_window, text="Select Payment Method:").pack(pady=5)
        method = ttk.Combobox(payment_window, values=["Cash", "Card"])
        method.pack(pady=5)

        # Process payment
        def finalize_payment():
            # Process payment logic here
            self.save_sale(method.get())
            self.generate_receipt()
            payment_window.destroy()
            self.clear_cart()
            messagebox.showinfo("Success", "Payment processed successfully")

        ttk.Button(payment_window, text="Confirm Payment",
                   command=finalize_payment).pack(pady=5)

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

    def save_sale(self, payment_method):
        total = sum(item['price'] * item['quantity'] for item in self.cart)

        # Create sale record
        sale_id = self.db.execute_query(
            "INSERT INTO Sales (user_id, total, payment_method) VALUES (?, ?, ?)",
            (self.user['id'], total, payment_method)
        )

        # Create sale items
        for item in self.cart:
            self.db.execute_query(
                '''INSERT INTO SaleItems (sale_id, product_id, quantity, price)
                   VALUES (?, ?, ?, ?)''',
                (sale_id, item['id'],
                 item['quantity'], item['price'])
            )

            # Update stock
            self.db.execute_query(
                "UPDATE Products SET stock = stock - ? WHERE id = ?",
                (item['quantity'], item['id'])
            )

    def generate_receipt(self):
        filename = f"receipts/receipt_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        c = canvas.Canvas(filename, pagesize=letter)

        # Receipt header
        c.setFont("Helvetica-Bold", 18)
        c.drawString(100, 750, "SUPERMARKET POS")
        c.setFont("Helvetica", 12)
        c.drawString(
            100, 730, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        c.drawString(100, 710, f"Cashier: {self.user['username']}")

        # Items
        y = 680
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, y, "Product")
        c.drawString(300, y, "Qty")
        c.drawString(400, y, "Price")
        c.drawString(500, y, "Total")

        c.setFont("Helvetica", 12)
        for item in self.cart:
            y -= 20
            c.drawString(100, y, item['name'])
            c.drawString(300, y, str(item['quantity']))
            c.drawString(400, y, f"₦{item['price']:.2f}")
            c.drawString(500, y, f"₦{item['price'] * item['quantity']:.2f}")

        # Total
        y -= 30
        total = sum(item['price'] * item['quantity'] for item in self.cart)
        c.drawString(400, y, "Total:")
        c.drawString(500, y, f"₦{total:.2f}")

        c.save()
