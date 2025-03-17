import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from gui.login import LoginScreen
from gui.cashier import CashierInterface
from gui.admin import AdminDashboard


class POSApp(ttk.Window):
    def __init__(self):
        theme = self.get_initial_theme()
        super().__init__(themename=theme)
        self.title("Supermarket POS")
        self.geometry("800x600")
        self.current_user = None
        self.show_login_screen()

        # Create the logout button but don't pack it yet
        self.logout_button = ttk.Button(
            self, text="Logout", command=self.log_out)

        # Create the exit button
        self.exit_button = ttk.Button(
            self, text="Exit", command=self.exit_app, bootstyle="danger")

        # Show the exit button
        self.exit_button.pack(side=RIGHT, anchor=NE, padx=10, pady=10)

    def log_out(self):
        self.current_user = None
        self.logout_button.pack_forget()  # Hide the logout button
        self.show_login_screen()

    def exit_app(self):
        self.destroy()  # Close the application

    def get_initial_theme(self):
        try:
            with open('theme.txt', 'r') as file:
                return file.read()
        except FileNotFoundError:
            return 'darkly'

    def show_login_screen(self):
        self.clear_frame()
        LoginScreen(self, self.on_login_success,
                    self.set_theme).pack(expand=True)

    def on_login_success(self, user):
        self.current_user = user
        # Show the logout button
        self.logout_button.pack(side=RIGHT, anchor=NE, padx=10, pady=10)

        if user['role'] == 'cashier':
            self.show_cashier_interface()
        else:
            self.show_admin_dashboard()

    def show_cashier_interface(self):
        self.clear_frame()
        CashierInterface(self, self.current_user).pack(fill=BOTH, expand=True)

    def show_admin_dashboard(self):
        self.clear_frame()
        AdminDashboard(self, self.current_user).pack(fill=BOTH, expand=True)

    def clear_frame(self):
        for widget in self.winfo_children():
            # Don't destroy the logout and exit buttons
            if widget not in [self.logout_button, self.exit_button]:
                widget.destroy()

    def set_theme(self, theme):
        self.style.theme_use(theme)


if __name__ == "__main__":
    app = POSApp()
    app.mainloop()
