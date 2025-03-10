# 🛒 Supermarket Payment Solution

Welcome to the **Supermarket Payment Solution**! This project is a comprehensive Point of Sale (POS) system designed to streamline supermarket operations, including inventory management, sales processing, and reporting.

## ✨ Features

- 🔐 **User Authentication**: Secure login for admins and cashiers.
- 📦 **Inventory Management**: Add, edit, and delete products.
- 💳 **Sales Processing**: Handle cash and card payments.
- 📊 **Reporting**: Generate daily sales and product performance reports.
- 🧾 **Receipt Generation**: Automatically generate PDF receipts for transactions.

## 📸 Screenshots

![Admin Dashboard](screenshots/admin_dashboard.png)
![Cashier Interface](screenshots/cashier_interface.png)

## ⚙️ Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/KhalifahMB/Supermarket-Payment-Solution.git
    cd supermarket-payment-solution
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv env
    ```

3. **Activate the virtual environment**:
    - On Windows:
        ```sh
        .\env\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source env/bin/activate
        ```

4. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    
5. **Uncomment and run the setup script**:
    - Open `script.py` and uncomment the necessary lines.
    - Run the script:
        ```sh
         python script.py
        ```
    - After running, comment the lines back in `script.py`.


6. **Run the application**:
    ```sh
    python main.py
    ```

## 🚀 Usage

- **Admin Login**: Use the credentials `username/password, admin/admin123` to log in as an admin.
- **Cashier Login**: Use the credentials `username/password, cashier1/cash123` to log in as a cashier.
