"""
seed_data.py
Generates realistic synthetic data for the E-commerce Sales Analytics
project and bulk-loads it into MySQL.

SETUP
-----
1. pip install faker pymysql
2. Run schema.sql first (creates the database + tables)
3. Update DB_CONFIG below with your MySQL credentials
4. python seed_data.py

This creates ~3,000 customers, 400 products, 25,000 orders (with
1-5 line items each), matching payments, and ~6% returns, spread
across roughly 2 years so month-over-month/trend queries have
enough data to actually show patterns.
"""

import random
from datetime import datetime, timedelta

import pymysql
from faker import Faker

fake = Faker("en_IN")  # Indian locale for realistic names/cities — change if needed
random.seed(42)
Faker.seed(42)

# ------------------------------------------------------------
# CONFIG — edit these
# ------------------------------------------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "password",
    "database": "ecommerce_analytics",
    "autocommit": False,
}

NUM_CUSTOMERS = 3000
NUM_SUPPLIERS = 100
NUM_PRODUCTS = 400
NUM_ORDERS = 25000
MAX_ITEMS_PER_ORDER = 5
RETURN_RATE = 0.06
START_DATE = datetime(2024, 6, 1)
END_DATE = datetime(2026, 8, 1)

CATEGORIES = {
    "Electronics": ["Mobiles", "Laptops", "Headphones", "Cameras"],
    "Fashion": ["Men's Wear", "Women's Wear", "Footwear", "Accessories"],
    "Home & Kitchen": ["Furniture", "Cookware", "Decor"],
    "Beauty": ["Skincare", "Haircare", "Makeup"],
    "Sports": ["Fitness Equipment", "Outdoor Gear", "Sportswear"],
    "Books": ["Fiction", "Non-Fiction", "Academic"],
    "Grocery": ["Snacks", "Beverages", "Staples"],
    "Toys": ["Educational", "Action Figures", "Board Games"],
}

PAYMENT_METHODS = ["Credit Card", "Debit Card", "UPI", "Net Banking", "COD"]
ORDER_STATUSES = ["Delivered", "Delivered", "Delivered", "Shipped", "Pending", "Cancelled"]
RETURN_REASONS = [
    "Defective product",
    "Wrong item delivered",
    "Size/fit issue",
    "Changed my mind",
    "Better price found elsewhere",
    "Late delivery",
]


def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))


def get_connection():
    return pymysql.connect(**DB_CONFIG)


def insert_customers(cursor, n):
    print(f"Generating {n} customers...")
    data = [
        (
            fake.name(),
            fake.unique.email(),
            fake.phone_number()[:20],
            fake.city(),
            fake.state(),
            random_date(START_DATE, END_DATE).date(),
        )
        for _ in range(n)
    ]
    cursor.executemany(
        """INSERT INTO customers (name, email, phone, city, state, signup_date)
           VALUES (%s, %s, %s, %s, %s, %s)""",
        data,
    )


def insert_suppliers(cursor, n):
    print(f"Generating {n} suppliers...")
    data = [(fake.company(), fake.city(), fake.state()) for _ in range(n)]
    cursor.executemany(
        "INSERT INTO suppliers (supplier_name, city, state) VALUES (%s, %s, %s)",
        data,
    )


def insert_products(cursor, n, num_suppliers):
    print(f"Generating {n} products...")
    data = []
    for _ in range(n):
        category = random.choice(list(CATEGORIES.keys()))
        sub_category = random.choice(CATEGORIES[category])
        cost = round(random.uniform(100, 8000), 2)
        price = round(cost * random.uniform(1.2, 2.5), 2)
        data.append(
            (
                f"{sub_category} {fake.word().capitalize()} {random.randint(100, 999)}",
                category,
                sub_category,
                price,
                cost,
                random.randint(1, num_suppliers),
            )
        )
    cursor.executemany(
        """INSERT INTO products (product_name, category, sub_category, price, cost, supplier_id)
           VALUES (%s, %s, %s, %s, %s, %s)""",
        data,
    )


def insert_orders_and_items(cursor, num_orders, num_customers, num_products):
    print(f"Generating {num_orders} orders with line items and payments...")
    items_batch = []
    payments_batch = []

    for i in range(num_orders):
        customer_id = random.randint(1, num_customers)
        order_date = random_date(START_DATE, END_DATE)
        status = random.choice(ORDER_STATUSES)

        cursor.execute(
            "INSERT INTO orders (customer_id, order_date, order_status) VALUES (%s, %s, %s)",
            (customer_id, order_date.date(), status),
        )
        order_id = cursor.lastrowid

        order_total = 0
        for _ in range(random.randint(1, MAX_ITEMS_PER_ORDER)):
            product_id = random.randint(1, num_products)
            quantity = random.randint(1, 4)
            unit_price = round(random.uniform(200, 15000), 2)
            discount = random.choice([0, 0, 0, 5, 10, 15, 20])
            order_total += quantity * unit_price * (1 - discount / 100)
            items_batch.append((order_id, product_id, quantity, unit_price, discount))

        payment_status = "Success" if status != "Cancelled" else random.choice(["Failed", "Refunded"])
        payments_batch.append(
            (order_id, random.choice(PAYMENT_METHODS), payment_status, order_date.date(), round(order_total, 2))
        )

        if len(items_batch) >= 5000:
            cursor.executemany(
                """INSERT INTO order_items (order_id, product_id, quantity, unit_price, discount)
                   VALUES (%s, %s, %s, %s, %s)""",
                items_batch,
            )
            items_batch = []

        if len(payments_batch) >= 2000:
            cursor.executemany(
                """INSERT INTO payments (order_id, payment_method, payment_status, payment_date, amount)
                   VALUES (%s, %s, %s, %s, %s)""",
                payments_batch,
            )
            payments_batch = []

        if (i + 1) % 5000 == 0:
            print(f"  ...{i + 1} orders inserted")

    if items_batch:
        cursor.executemany(
            """INSERT INTO order_items (order_id, product_id, quantity, unit_price, discount)
               VALUES (%s, %s, %s, %s, %s)""",
            items_batch,
        )
    if payments_batch:
        cursor.executemany(
            """INSERT INTO payments (order_id, payment_method, payment_status, payment_date, amount)
               VALUES (%s, %s, %s, %s, %s)""",
            payments_batch,
        )


def insert_returns(cursor, return_rate):
    print("Generating returns...")
    cursor.execute("SELECT order_item_id, unit_price, quantity FROM order_items")
    all_items = cursor.fetchall()
    sample_size = int(len(all_items) * return_rate)
    sampled = random.sample(all_items, sample_size)

    data = []
    for order_item_id, unit_price, quantity in sampled:
        return_date = fake.date_between(start_date="-18M", end_date="today")
        refund_amount = round(float(unit_price) * quantity * random.uniform(0.8, 1.0), 2)
        data.append((order_item_id, return_date, random.choice(RETURN_REASONS), refund_amount))

    cursor.executemany(
        """INSERT INTO returns (order_item_id, return_date, return_reason, refund_amount)
           VALUES (%s, %s, %s, %s)""",
        data,
    )
    return len(data)


def main():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        insert_customers(cursor, NUM_CUSTOMERS)
        insert_suppliers(cursor, NUM_SUPPLIERS)
        insert_products(cursor, NUM_PRODUCTS, NUM_SUPPLIERS)
        conn.commit()
        print("Customers, suppliers, and products committed.")

        insert_orders_and_items(cursor, NUM_ORDERS, NUM_CUSTOMERS, NUM_PRODUCTS)
        conn.commit()
        print("Orders, order_items, and payments committed.")

        num_returns = insert_returns(cursor, RETURN_RATE)
        conn.commit()
        print(f"{num_returns} returns committed.")

        print("\nData generation complete.")

    except Exception as e:
        conn.rollback()
        print(f"Error occurred, rolled back: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()