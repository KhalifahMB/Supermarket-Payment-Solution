from database import DatabaseManager
from matplotlib.figure import Figure
import math


def daily_sales(db, start, end):
    data = db.execute_query('''
                SELECT DATE(timestamp) AS date, SUM(total) AS total
                FROM Sales
                WHERE date BETWEEN ? AND ?
                GROUP BY date
            ''', (start, end), fetch=True)
    fig = Figure()
    ax = fig.add_subplot(111)
    dates = [row['date'] for row in data]
    totals = [row['total'] for row in data]
    ax.bar(dates, totals)
    ax.set_title("Daily Sales Report")

    return fig


def product_performance(db):
    data = db.execute_query('''
                SELECT product_id as product, SUM(price * quantity) as total_price
                 FROM SaleItems
                GROUP BY product_id
                LIMIT 10
            ''',  fetch=True)

    product_data = db.execute_query('''
        SELECT * FROM Products
    ''',  fetch=True)
    product_dict = {}
    for row in product_data:
        for product in data:
            if product['product'] == row['id']:
                values = [row['name'], product['total_price']]
                product_dict[row['id']] = values

    fig = Figure()
    ax = fig.add_subplot(111)
    x = [x[1] for x in product_dict.values()]
    y = [math.floor(y[1]) for y in product_dict.values()]
    ax.pie(x=x, data=product_dict, labels=y)
    ax.set_title("Product Sale Performance")
    legend = [y[0] for y in product_dict.values()]
    ax.legend(labels=legend, loc='lower left', bbox_to_anchor=(1, 0, 0.5, 1))

    return fig
