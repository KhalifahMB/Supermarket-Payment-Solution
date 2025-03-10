import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from database import DatabaseManager
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import messagebox
from datetime import datetime


class AdminDashboard(ttk.Frame):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user
        self.db = DatabaseManager()
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        notebook = ttk.Notebook(main_frame)

        # Inventory Management Tab
        inventory_tab = ttk.Frame(notebook)
        self.create_inventory_management(inventory_tab)
        notebook.add(inventory_tab, text="Inventory")

        # Reports Tab
        reports_tab = ttk.Frame(notebook)
        self.create_reports_interface(reports_tab)
        notebook.add(reports_tab, text="Reports")

        notebook.pack(fill=BOTH, expand=True)

    def create_inventory_management(self, parent):
        # Product List
        self.inventory_tree = ttk.Treeview(parent, columns=(
            'id', 'name', 'price', 'stock'), show='headings')
        self.inventory_tree.heading('id', text='ID')
        self.inventory_tree.heading('name', text='Product')
        self.inventory_tree.heading('price', text='Price')
        self.inventory_tree.heading('stock', text='Stock')
        self.inventory_tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Control Buttons
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Add Product",
                   command=self.show_add_product_dialog).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Edit Product",
                   command=self.show_edit_product_dialog).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Product",
                   command=self.delete_product).pack(side=LEFT, padx=5)

        self.load_inventory()

    def load_inventory(self):
        self.inventory_tree.delete(*self.inventory_tree.get_children())
        products = self.db.execute_query("SELECT * FROM Products", fetch=True)
        for product in products:
            self.inventory_tree.insert('', 'end', values=(
                product['id'],
                product['name'],
                f"₦{product['price']:.2f}",
                product['stock']
            ))

    def create_reports_interface(self, parent):
        report_frame = ttk.Frame(parent)
        report_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Report Type Selection
        ttk.Label(report_frame, text="Select Report:").pack(
            side=TOP, anchor=NW)
        self.report_type = ttk.Combobox(
            report_frame, values=["Daily Sales", "Product Performance"])
        self.report_type.pack(side=TOP, anchor=NW, pady=5)

        # Date Range Selector
        date_frame = ttk.Frame(report_frame)
        date_frame.pack(side=TOP, fill=X, pady=5)

        ttk.Label(date_frame, text="From:").pack(side=LEFT)
        self.start_date = ttk.DateEntry(date_frame)
        self.start_date.pack(side=LEFT, padx=5)

        ttk.Label(date_frame, text="To:").pack(side=LEFT)
        self.end_date = ttk.DateEntry(date_frame)
        self.end_date.pack(side=LEFT, padx=5)

        # Generate Report Button
        ttk.Button(report_frame, text="Generate Report",
                   command=self.generate_report).pack(side=TOP, pady=10)

        # Chart Display Area
        self.chart_canvas = FigureCanvasTkAgg(Figure(), report_frame)
        self.chart_canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    def generate_report(self):
        report_type = self.report_type.get()
        start = self.start_date.entry.get()
        end = self.end_date.entry.get()
        start = datetime.strptime(start, '%d/%m/%Y')
        end = datetime.strptime(end, '%d/%m/%Y')
        if report_type == "Daily Sales":
            data = self.db.execute_query('''
                SELECT DATE(timestamp) AS date, SUM(total) AS total
                FROM Sales
                WHERE date BETWEEN ? AND ?
                GROUP BY date
            ''', (start, end), fetch=True)
            fig = Figure()
            ax = fig.add_subplot(111)
            dates = [row['date'] for row in data]
            totals = [row['total'] for row in data]
            ax.bar(dates, totals)
            ax.set_title("Daily Sales Report")
            self.chart_canvas.figure = fig
            self.chart_canvas.draw()
        elif report_type == "Product Performance":
            data = self.db.execute_query('''
                SELECT Date(timestamp) as date, SUM(total) as total
                FROM Sales
                WHERE date BETWEEN Date(?) AND Date(?)
                GROUP BY date
            ''', (start, end), fetch=True)
            fig = Figure()
            ax = fig.add_subplot(111)
            date = [row['date'] for row in data]
            total_sale = [row['total'] for row in data]
            ax.bar(date, total_sale)
            ax.set_title("Daily Sales Report")
            self.chart_canvas.figure = fig
            self.chart_canvas.draw()

    def show_add_product_dialog(self):
        dialog = ttk.Toplevel(self)
        dialog.title("Add New Product")

        ttk.Label(dialog, text="Product Name:").grid(
            row=0, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(dialog)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Price:").grid(row=1, column=0, padx=5, pady=5)
        price_entry = ttk.Entry(dialog)
        price_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Initial Stock:").grid(
            row=2, column=0, padx=5, pady=5)
        stock_entry = ttk.Entry(dialog)
        stock_entry.grid(row=2, column=1, padx=5, pady=5)

        def save_product():
            name = name_entry.get()
            price = price_entry.get()
            stock = stock_entry.get()

            if not name or not price or not stock:
                messagebox.showerror("Error", "All fields are required")
                return

            try:
                price = float(price)
                stock = int(stock)
            except ValueError:
                messagebox.showerror("Error", "Invalid price or stock value")
                return

            self.db.execute_query(
                "INSERT INTO Products (name, price, stock) VALUES (?, ?, ?)",
                (name, price, stock)
            )
            self.load_inventory()
            dialog.destroy()

        ttk.Button(dialog, text="Save", command=save_product).grid(
            row=3, columnspan=2, pady=10)

    def show_edit_product_dialog(self):
        selected = self.inventory_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required",
                                   "Please select a product to edit")
            return

        product_id = self.inventory_tree.item(selected[0], 'values')[0]
        product = self.db.execute_query(
            "SELECT * FROM Products WHERE id = ?",
            (product_id,),
            fetch=True
        )[0]

        dialog = ttk.Toplevel(self)
        dialog.title("Edit Product")

        ttk.Label(dialog, text="Product Name:").grid(
            row=0, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(dialog)
        name_entry.insert(0, product['name'])
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Price:").grid(row=1, column=0, padx=5, pady=5)
        price_entry = ttk.Entry(dialog)
        price_entry.insert(0, str(product['price']))
        price_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Stock:").grid(row=2, column=0, padx=5, pady=5)
        stock_entry = ttk.Entry(dialog)
        stock_entry.insert(0, str(product['stock']))
        stock_entry.grid(row=2, column=1, padx=5, pady=5)

        def save_changes():
            name = name_entry.get()
            price = price_entry.get()
            stock = stock_entry.get()

            if not name or not price or not stock:
                messagebox.showerror("Error", "All fields are required")
                return

            try:
                price = float(price)
                stock = int(stock)
            except ValueError:
                messagebox.showerror("Error", "Invalid price or stock value")
                return

            self.db.execute_query(
                "UPDATE Products SET name = ?, price = ?, stock = ? WHERE id = ?",
                (name, price, stock, product_id)
            )
            self.load_inventory()
            dialog.destroy()

        ttk.Button(dialog, text="Save Changes", command=save_changes).grid(
            row=3, columnspan=2, pady=10)

    def delete_product(self):
        selected = self.inventory_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required",
                                   "Please select a product to delete")
            return

        product_id = self.inventory_tree.item(selected[0], 'values')[0]

        confirm = messagebox.askyesno(
            "Confirm Delete", "Are you sure you want to delete this product?")
        if confirm:
            self.db.execute_query(
                "DELETE FROM Products WHERE id = ?", (product_id,))
            self.load_inventory()
