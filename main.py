import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from gui.login import LoginScreen
from gui.cashier import CashierInterface
from gui.admin import AdminDashboard


class POSApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="superhero")
        self.title("Supermarket POS")
        self.geometry("1200x800")
        self.current_user = None
        self.show_login_screen()

    def show_login_screen(self):
        self.clear_frame()
        LoginScreen(self, self.on_login_success).pack(expand=True)

    def on_login_success(self, user):
        self.current_user = user
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
            widget.destroy()


if __name__ == "__main__":
    app = POSApp()
    app.mainloop()
