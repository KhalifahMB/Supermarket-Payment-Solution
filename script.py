from auth import AuthSystem
from database import DatabaseManager
from sqlite3 import Date
import random
from datetime import datetime, timedelta
import os
import math
import hashlib
from utils.cart import sale_save, save_saleitem, get_product
db = DatabaseManager()

product_names = [
    'Coca-Cola 500ml', 'Indomie Chicken 70g', 'Pepsi 500ml', 'Lays Chips', 'Oreo Biscuits',
    'Sprite 500ml', 'Mountain Dew 500ml', 'Fanta 500ml', '7Up 500ml', 'Mirinda 500ml',
    'Pringles Original', 'Pringles Sour Cream', 'Pringles BBQ', 'Doritos Nacho Cheese', 'Doritos Cool Ranch',
    'KitKat 4 Finger', 'Snickers Bar', 'Mars Bar', 'Twix Bar', 'Bounty Bar',
    'Cadbury Dairy Milk', 'Cadbury Fruit & Nut', 'Cadbury Caramel', 'Galaxy Smooth Milk', 'Galaxy Caramel',
    'Nestle Crunch', 'Nestle Milkybar', 'Nestle Aero', 'Nestle KitKat Chunky', 'Nestle Lion Bar',
    'Hershey\'s Milk Chocolate', 'Hershey\'s Cookies \'n\' Creme', 'Hershey\'s Almond', 'Hershey\'s Dark Chocolate', 'Hershey\'s Gold',
    'M&M\'s Peanut', 'M&M\'s Chocolate', 'M&M\'s Crispy', 'Skittles Original', 'Skittles Sour',
    'Haribo Goldbears', 'Haribo Starmix', 'Haribo Tangfastics', 'Haribo Happy Cola', 'Haribo Twin Snakes',
    'Lay\'s Classic', 'Lay\'s Sour Cream & Onion', 'Lay\'s BBQ', 'Lay\'s Salt & Vinegar', 'Lay\'s Cheddar & Sour Cream',
    'Ruffles Original', 'Ruffles Cheddar & Sour Cream', 'Ruffles BBQ', 'Ruffles Sour Cream & Onion', 'Ruffles All Dressed'
]

# def generate_random_sales_data():
#     sales_data = []
#     start_date = datetime(2020, 1, 1)
#     end_date = datetime(2025, 3, 9)
#     for _ in range(10):
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

# def generate_random_product_data():
#     product_data = []
#     for product in product_names:
#         name = product
#         price = round(random.uniform(100, 500), 2)
#         stock = random.randint(20, 100)
#         low_stock_threshold = random.randint(5, 20)
#         product_data.append((name, price, stock, low_stock_threshold))
#     return product_data
# product_data = generate_random_product_data()
# for product in product_data:
#     db.execute_query(
#         "INSERT OR IGNORE INTO Products (name, price, stock, low_stock_threshold) VALUES (?, ?, ?, ?)", product)

# db.execute_query("INSERT OR IGNORE INTO Users VALUES (?, ?, ?, ?)",
#                  (1, 'Muhammad', 'admin123', 'admin'))
# db.execute_query("INSERT OR IGNORE INTO Users VALUES (?, ?, ?, ?)",
#                  (2, 'Usman', 'cash123', 'cashier'))


# sales_data = db.execute_query('''
#                 SELECT DATE(timestamp) AS date, SUM(total) AS total
#                 FROM Sales
#                 ''', fetch=True)

# for sale in sales_data:
#     print(sale['date'], sale:)

# def get_products():
#     data = db.execute_query('''
#                 SELECT product_id, SUM(price * quantity) as total_price
#                  FROM SaleItems
#                 GROUP BY product_id
#             ''',  fetch=True)
#     return data


# products_info = []
# products = get_products()
# for row in products:
#     product = []
#     product.append(row['product_id'])
#     product.append(row['total_price'])
#     products_info.append(product)

# print(products_info)

# def get_products_as_dict():
#     data = db.execute_query('''
#                             SELECT product_id as product, SUM(price * quantity) as total_price
#                             FROM SaleItems
#                             GROUP BY product_id
#                         ''',  fetch=True)
#     product_data = db.execute_query('''
#                 SELECT * FROM Products
#             ''',  fetch=True)
#     product_dict = {}
#     for row in product_data:
#         for product in data:
#             if product['product'] == row['id']:
#                 values = [row['name'], product['total_price']]
#                 product_dict[row['id']] = values
#     x = [product_dict[x][1] for x in product_dict]
#     y = [product_dict[y][0] for y in product_dict]
#     print(product_dict)
#     print(x)
#     print(y)


# get_products_as_dict()


# items = []
# for i in range(len(product_names) + 1):
#     item = {}
#     id = random.randint(i, len(product_names))
#     item['id'] = id
#     item['quantity'] = random.randint(2, 10)
#     item['price'] = get_product(db, id)['price']
#     items.append(item)

# for item in items:
#     sale_item = save_saleitem(
#         db=db, order_id=item['id'] * item['price'], item=item)

# def hash_passtword(password: str) -> str:
# Hashes a password using SHA-256 and returns the hashed password
#     return hashlib.sha256(password.encode()).hexdigest()


# password = hash_password(password='cash123')
# print(password)

# db.execute_query(
#     "UPDATE Users SET password = ?  WHERE id = ?",
#     (password, 2)
# )
