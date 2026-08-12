-- ============================================================
-- E-commerce / Retail Sales Analytics System — Schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS ecommerce_analytics;
USE ecommerce_analytics;

-- Drop tables if re-running (children first, to respect FK constraints)
DROP TABLE IF EXISTS returns;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS suppliers;
DROP TABLE IF EXISTS customers;

-- ------------------------------------------------------------
-- customers
-- ------------------------------------------------------------
CREATE TABLE customers (
    customer_id   INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    email         VARCHAR(150) NOT NULL UNIQUE,
    phone         VARCHAR(20),
    city          VARCHAR(50),
    state         VARCHAR(50),
    signup_date   DATE NOT NULL
);

-- ------------------------------------------------------------
-- suppliers
-- ------------------------------------------------------------
CREATE TABLE suppliers (
    supplier_id   INT AUTO_INCREMENT PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    city          VARCHAR(50),
    state         VARCHAR(50)
);

-- ------------------------------------------------------------
-- products
-- ------------------------------------------------------------
CREATE TABLE products (
    product_id    INT AUTO_INCREMENT PRIMARY KEY,
    product_name  VARCHAR(150) NOT NULL,
    category      VARCHAR(50) NOT NULL,
    sub_category  VARCHAR(50),
    price         DECIMAL(10,2) NOT NULL,
    cost          DECIMAL(10,2) NOT NULL,
    supplier_id   INT,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
        ON DELETE SET NULL
);

-- ------------------------------------------------------------
-- orders
-- ------------------------------------------------------------
CREATE TABLE orders (
    order_id      INT AUTO_INCREMENT PRIMARY KEY,
    customer_id   INT NOT NULL,
    order_date    DATE NOT NULL,
    order_status  ENUM('Pending','Shipped','Delivered','Cancelled') NOT NULL DEFAULT 'Pending',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        ON DELETE CASCADE
);

-- ------------------------------------------------------------
-- order_items
-- ------------------------------------------------------------
CREATE TABLE order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id      INT NOT NULL,
    product_id    INT NOT NULL,
    quantity      INT NOT NULL,
    unit_price    DECIMAL(10,2) NOT NULL,
    discount      DECIMAL(5,2) DEFAULT 0,      -- percentage, e.g. 10.00 = 10%
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE RESTRICT
);

-- ------------------------------------------------------------
-- payments  (1-to-1 with orders)
-- ------------------------------------------------------------
CREATE TABLE payments (
    payment_id      INT AUTO_INCREMENT PRIMARY KEY,
    order_id        INT NOT NULL UNIQUE,
    payment_method  ENUM('Credit Card','Debit Card','UPI','Net Banking','COD') NOT NULL,
    payment_status  ENUM('Success','Failed','Pending','Refunded') NOT NULL,
    payment_date    DATE NOT NULL,
    amount          DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON DELETE CASCADE
);

-- ------------------------------------------------------------
-- returns
-- ------------------------------------------------------------
CREATE TABLE returns (
    return_id      INT AUTO_INCREMENT PRIMARY KEY,
    order_item_id  INT NOT NULL,
    return_date    DATE NOT NULL,
    return_reason  VARCHAR(255),
    refund_amount  DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_item_id) REFERENCES order_items(order_item_id)
        ON DELETE CASCADE
);

-- ------------------------------------------------------------
-- Indexes to speed up the analytical queries you'll run later
-- ------------------------------------------------------------
CREATE INDEX idx_orders_date        ON orders(order_date);
CREATE INDEX idx_orders_customer    ON orders(customer_id);
CREATE INDEX idx_items_order        ON order_items(order_id);
CREATE INDEX idx_items_product      ON order_items(product_id);
CREATE INDEX idx_products_category  ON products(category);
CREATE INDEX idx_payments_status    ON payments(payment_status);