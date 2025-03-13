from database import DatabaseManager
from sqlite3 import Date
import random
from datetime import datetime, timedelta
import os
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

# api_key = os.getenv('SECRET_KEY')
# print(os.getenv("SECRET_KEY"))
# print(f'api_key: {api_key}')
# print(os.getenv('SQUARE_ACCESS_TOKEN'))
print(os.getenv('SQUARE_LOCATION_ID'))
