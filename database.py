import sqlite3
from contextlib import contextmanager
from typing import Generator, List, Tuple, Any, Optional


class DatabaseManager:
    def __init__(self, db_name: str = 'supermarket.db') -> None:
        self.db_name = db_name
        self.initialize_db()

    def initialize_db(self) -> None:
        # Create tables if they do not exist
        with self.get_cursor() as cursor:
            # Create Users table with id, username, password, and role columns
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    password TEXT,
                    role TEXT CHECK(role IN ('admin', 'cashier'))
                )''')

            # Create Products table with id, name, price, stock, and low_stock_threshold columns
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Products (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE,
                    price REAL,
                    stock INTEGER,
                    low_stock_threshold INTEGER DEFAULT 5
                )''')

            # Create Sales table with id, user_id, total, payment_method, and timestamp columns
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Sales (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    total REAL,
                    payment_method TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')

            # Create SaleItems table with sale_id, product_id, quantity, price, and timestamp columns
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS SaleItems (
                    order_id INTEGER,
                    product_id INTEGER,
                    quantity INTEGER,
                    price REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')

    @contextmanager
    def get_cursor(self) -> Generator[sqlite3.Cursor, None, None]:
        # Context manager to get a database cursor
        conn = sqlite3.connect(self.db_name)

        # Set row factory to sqlite3.Row for dictionary-like row access
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        finally:
            conn.close()

    def execute_query(self, query: str, params: Tuple[Any, ...] = (), fetch: bool = False) -> Optional[List[sqlite3.Row]]:
        # Execute a query with optional parameters and fetch results if needed
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            if fetch:
                # Fetch and return all results if fetch is True
                return cursor.fetchall()
        return None
