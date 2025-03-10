from database import DatabaseManager
from sqlite3 import Date
import random
from datetime import datetime, timedelta
import math

db = DatabaseManager()


# def generate_random_sales_data():
#     sales_data = []
#     start_date = datetime(2020, 1, 1)
#     end_date = datetime(2025, 3, 9)
#     for _ in range(20):
#         user_id = random.choice([1, 2])
#         total = math.floor(random.uniform(250, 100000))
#         payment_method = random.choice(['Cash', 'Card'])
#         timestamp = (start_date + (end_date - start_date) *
#                      random.random()).replace(microsecond=0)
#         sales_data.append((user_id, total, payment_method, timestamp))
#     return sales_data


# sales_data = generate_random_sales_data()
# for sale in sales_data:
#     data = db.execute_query(
#         "INSERT INTO Sales (user_id,total,  payment_method, timestamp) VALUES (?, ?, ?, ?)", sale)


# db.execute_query("INSERT OR IGNORE INTO Users VALUES (?, ?, ?, ?)",
#                  (1, 'admin', 'admin123', 'admin'))
# db.execute_query("INSERT OR IGNORE INTO Users VALUES (?, ?, ?, ?)",
#                  (2, 'cashier1', 'cash123', 'cashier'))
# db.execute_query("INSERT OR IGNORE INTO Products VALUES (?, ?, ?, ?, ?)",
#                  (1, 'Coca-Cola 500ml', 250.0, 100, 10))
# db.execute_query("INSERT OR IGNORE INTO Products VALUES (?, ?, ?, ?, ?)",
#                  (2, 'Indomie Chicken 70g', 150.0, 50, 5))

# data = db.execute_query('''
#                 SELECT DATE(timestamp) AS date, SUM(total) AS total
#                 FROM Sales
#                 ''', fetch=True)
