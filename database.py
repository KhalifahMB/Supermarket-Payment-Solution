import sqlite3
from contextlib import contextmanager


class DatabaseManager:
    def __init__(self, db_name='supermarket.db'):
        self.db_name = db_name
        self.initialize_db()

    def initialize_db(self):
        with self.get_cursor() as cursor:
            # Create tables if not exists
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    password TEXT,
                    role TEXT CHECK(role IN ('admin', 'cashier'))
                )''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Products (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE,
                    price REAL,
                    stock INTEGER,
                    low_stock_threshold INTEGER DEFAULT 5
                )''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Sales (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    total REAL,
                    payment_method TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS SaleItems (
                    sale_id INTEGER,
                    product_id INTEGER,
                    quantity INTEGER,
                    price REAL
                )''')

    @contextmanager
    def get_cursor(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        finally:
            conn.close()

    def execute_query(self, query, params=(), fetch=False):
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            if fetch:
                return cursor.fetchall()
