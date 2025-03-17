from datetime import datetime


def product_search(db, query):
    products = db.execute_query(
        "SELECT * FROM Products WHERE name LIKE ? OR id = ?", (f"%{query}%", query), fetch=True)

    return products


def get_product(db, product_id):
    product = db.execute_query(
        "SELECT * FROM Products WHERE id = ?", (product_id,), fetch=True)[0]

    return product


def sale_save(db, user_id, total, method):
    sale_id = db.execute_query(
        "INSERT INTO Sales (user_id, total, payment_method) VALUES (?, ?, ?)",
        (user_id, total, method)
    )
    return sale_id


def save_saleitem(db, order_id, item):
    data = db.execute_query(
        '''INSERT INTO SaleItems (order_id, product_id, quantity, price)
                VALUES (?, ?, ?, ?)''',
        (order_id, item['id'], item['quantity'], item['price'])
    )
    return data


def update_productstock(db, item):
    db.execute_query(
        "UPDATE Products SET stock = stock - ? WHERE id = ?",
        (item['quantity'], item['id'])
    )
