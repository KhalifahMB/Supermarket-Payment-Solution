import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from database import DatabaseManager
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import messagebox, simpledialog
from datetime import datetime
from utils.report import product_performance, daily_sales
from auth import AuthSystem


class AdminDashboard(ttk.Frame):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user
        self.db = DatabaseManager()
        self.page_size = 20  # Number of items per page
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

        # User Management Tab
        user_tab = ttk.Frame(notebook)
        self.create_user_management(user_tab)
        notebook.add(user_tab, text="Users")

        notebook.pack(fill=BOTH, expand=True)

    def create_inventory_management(self, parent):
        # Product List
        self.inventory_table = Tableview(
            parent,
            coldata=[
                {"text": "ID", "stretch": True, 'width': 20},
                {"text": "ProductName", "stretch": False},
                {"text": "Price", "stretch": True},
                {"text": "Stock", "stretch": True},
            ],
            rowdata=[],
            paginated=True,
            searchable=True,
            bootstyle=PRIMARY,
            pagesize=self.page_size,
        )
        self.inventory_table.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Control Buttons
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Add Product",
                   command=self.show_add_product_dialog).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Edit Product",
                   command=self.show_edit_product_dialog).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Product",
                   command=lambda: self.delete_item(self.inventory_table, "Products")).pack(side=LEFT, padx=5)

        self.load_inventory()

    def load_inventory(self):
        self.inventory_table.delete_rows()  # Clear existing rows
        products = self.db.execute_query("SELECT * FROM Products", fetch=True)
        for product in products:
            values = [product['id'], product['name'],
                      f"₦{product['price']:.2f}", product['stock']]
            self.inventory_table.insert_row('end', values)
        self.inventory_table.load_table_data()

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
        start_date = self.start_date.entry.get()
        end_date = self.end_date.entry.get()
        start_date = datetime.strptime(start_date, '%d/%m/%Y')
        end_date = datetime.strptime(end_date, '%d/%m/%Y')
        if report_type == "Daily Sales":
            fig = daily_sales(self.db, start_date, end_date)
            self.chart_canvas.figure = fig
            self.chart_canvas.draw()
        elif report_type == "Product Performance":
            fig = product_performance(self.db)
            self.chart_canvas.figure = fig
            self.chart_canvas.draw()

    def create_user_management(self, parent):
        # User List
        self.user_table = Tableview(
            parent,
            coldata=[
                {"text": "ID", "stretch": True, 'minwidth': 20},
                {"text": "Username", "stretch": True},
                {"text": "Role", "stretch": False},
            ],
            rowdata=[],
            searchable=True,
            paginated=True,
            pagesize=self.page_size,
        )
        self.user_table.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Control Buttons
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Add User",
                   command=self.show_add_user_dialog).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Edit User",
                   command=self.show_edit_user_dialog).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete User",
                   command=lambda: self.delete_item(self.user_table, "Users")).pack(side=LEFT, padx=5)

        self.load_users()

    def load_users(self):
        self.user_table.delete_rows()  # Clear existing rows
        users = self.db.execute_query("SELECT * FROM Users", fetch=True)
        for user in users:
            self.user_table.insert_row(
                'end',  # Parent row (empty for root)
                values=(user['id'], user['username'], user['role'])
            )
        self.user_table.load_table_data()

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
        selected = self.get_selected_product()
        if not selected:
            return

        dialog = ttk.Toplevel(self)
        dialog.title("Edit Product")

        ttk.Label(dialog, text="Product Name:").grid(
            row=0, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(dialog)
        name_entry.insert(0, selected['name'])
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Price:").grid(row=1, column=0, padx=5, pady=5)
        price_entry = ttk.Entry(dialog)
        price_entry.insert(0, str(selected['price']).replace(
            '₦', '').replace(',', ''))
        price_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Stock:").grid(row=2, column=0, padx=5, pady=5)
        stock_entry = ttk.Entry(dialog)
        stock_entry.insert(0, str(selected['stock']))
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
                (name, price, stock, selected['id'])
            )
            self.load_inventory()
            dialog.destroy()

        ttk.Button(dialog, text="Save Changes", command=save_changes).grid(
            row=3, columnspan=2, pady=10)

    def show_add_user_dialog(self):
        dialog = ttk.Toplevel(self)
        dialog.title("Add New User")

        ttk.Label(dialog, text="Username:").grid(
            row=0, column=0, padx=5, pady=5)
        username_entry = ttk.Entry(dialog)
        username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Password:").grid(
            row=1, column=0, padx=5, pady=5)
        password_entry = ttk.Entry(dialog, show="*")
        password_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Role:").grid(row=2, column=0, padx=5, pady=5)
        role_entry = ttk.Combobox(dialog, values=["admin", "cashier"])
        role_entry.grid(row=2, column=1, padx=5, pady=5)

        def save_user():
            username = username_entry.get()
            password = password_entry.get()
            role = role_entry.get()

            if not username or not password or not role:
                messagebox.showerror("Error", "All fields are required")
                return

            hashed_password = AuthSystem.hash_password(self, password)
            self.db.execute_query(
                "INSERT INTO Users (username, password, role) VALUES (?, ?, ?)",
                (username, hashed_password, role)
            )
            self.load_users()
            dialog.destroy()

        ttk.Button(dialog, text="Save", command=save_user).grid(
            row=3, columnspan=2, pady=10)

    def show_edit_user_dialog(self):
        selected = self.get_selected_user()
        if not selected:
            return

        dialog = ttk.Toplevel(self)
        dialog.title("Edit User")

        ttk.Label(dialog, text="Username:").grid(
            row=0, column=0, padx=5, pady=5)
        username_entry = ttk.Entry(dialog)
        username_entry.insert(0, selected['username'])
        username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Password:").grid(
            row=1, column=0, padx=5, pady=5)
        password_entry = ttk.Entry(dialog, show="*")
        password_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Role:").grid(row=2, column=0, padx=5, pady=5)
        role_entry = ttk.Combobox(dialog, values=["admin", "cashier"])
        role_entry.set(selected['role'])
        role_entry.grid(row=2, column=1, padx=5, pady=5)

        def save_changes():
            username = username_entry.get()
            password = password_entry.get()
            role = role_entry.get()

            if not username or not role:
                messagebox.showerror("Error", "Username and role are required")
                return

            if password:
                hashed_password = AuthSystem.hash_password(self, password)
                self.db.execute_query(
                    "UPDATE Users SET username = ?, password = ?, role = ? WHERE id = ?",
                    (username, hashed_password, role, selected['id'])
                )
                self.load_users()
            else:
                self.db.execute_query(
                    "UPDATE Users SET username = ?, role = ? WHERE id = ?",
                    (username, role, selected['id'])
                )
                self.load_users()
            dialog.destroy()

        ttk.Button(dialog, text="Save Changes", command=save_changes).grid(
            row=3, columnspan=2, pady=10)

    def delete_item(self, table, table_name):
        selected = table.view.selection()
        if not selected:
            messagebox.showwarning("Selection Required",
                                   f"Please select an item to delete")
            return
        selected = selected[0]
        row = table.get_row(iid=selected).values
        item_id = row[0]

        confirm = messagebox.askyesno(
            "Confirm Delete", f"Are you sure you want to delete this item?")
        if confirm:
            self.db.execute_query(
                f"DELETE FROM {table_name} WHERE id = ?", (item_id,))
            if table_name == "Users":
                self.load_users()
            else:
                self.load_inventory()

    def get_selected_product(self):
        selected = self.inventory_table.view.selection()
        if not selected:
            messagebox.showwarning("Selection Required",
                                   "Please select a product to edit")
            return None
        selected = selected[0]
        row = self.inventory_table.get_row(iid=selected).values
        return {"id": row[0], "name": row[1], "price": row[2], "stock": row[3]}

    def get_selected_user(self):
        selected = self.user_table.view.selection()
        if not selected:
            messagebox.showwarning("Selection Required",
                                   "Please select a user to edit")
            return None
        selected = selected[0]
        row = self.user_table.get_row(iid=selected).values
        return {"id": row[0], "username": row[1], "role": row[2]}
