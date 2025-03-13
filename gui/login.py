import ttkbootstrap as ttk
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.constants import *
from auth import AuthSystem
from tkinter import messagebox, StringVar


class LoginScreen(ttk.Frame):
    def __init__(self, parent, on_login, set_theme):
        super().__init__(parent)
        self.on_login = on_login
        self.auth = AuthSystem()
        self.set_theme = set_theme
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Login", style='Header.TLabel').grid(
            row=0, column=0,
            columnspan=2, pady=20, )

        ttk.Label(self, text="Select Theme:").grid(
            row=1, column=0, padx=5, pady=5)
        self.theme_var = StringVar(value='darkly')
        self.theme_combobox = ttk.Combobox(
            self, textvariable=self.theme_var, values=ttk.Style().theme_names())
        self.theme_combobox.grid(row=1, column=1, padx=5, pady=5)
        # Bind the selection event
        self.theme_combobox.bind("<<ComboboxSelected>>", self.update_theme)

        ttk.Label(self, text="Username:").grid(row=2, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self, text="Password:").grid(row=3, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=3, column=1, padx=5, pady=5)

        login_btn = ttk.Button(self, text="Login", command=self.attempt_login)
        login_btn.grid(row=4, column=0, columnspan=2, pady=20)

    def update_theme(self, event):
        theme = self.theme_var.get()
        self.set_theme(theme)
        with open('theme.txt', 'w') as file:
            file.write(theme)

    def attempt_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if (not username) or (not password):
            message_box = Messagebox()
            message_box.show_warning(
                message='Username and password field are required', title="Required Field ", parent=self, alert=True, )
            return
        user = self.auth.login(username, password)
        if not user:
            message_box = Messagebox()
            message_box.show_warning(
                message='Please provide a valid user credentials', title="Invalid Credentials", parent=self, alert=True, )
        else:
            self.on_login(user)
