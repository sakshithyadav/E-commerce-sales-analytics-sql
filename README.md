E-commerce Sales Analytics System
Project Overview

The E-commerce Sales Analytics System is a SQL-based data analytics project designed to analyze customer behavior, revenue trends, product performance, returns, and payment failures.

The project uses a relational database containing 7 interconnected tables:

Customers
Suppliers
Products
Orders
Order Items
Payments
Returns

Synthetic e-commerce data is generated using Python and Faker and loaded into MySQL for analysis.

The project focuses on solving real-world business questions using SQL techniques such as joins, window functions, conditional aggregation, CTEs, and stored procedures.

Objective:

The objective of this project is to analyze the E-commerce Sales Analytics database and uncover actionable insights related to:

Customer value and segmentation
Revenue trends and growth
Product performance
Product return patterns
Payment failure patterns
Monthly sales reporting

The analysis uses complex multi-table SQL queries across the seven interconnected tables to support business decisions related to marketing, inventory management, and checkout optimization.

Business Questions:

The project answers the following six key business questions:

Is revenue growing or declining month over month?
Which customers are VIP, regular, or at risk of churn?
What are the top 3 products per category by revenue?
Which product categories have the highest return rates?
Which payment methods have the highest failure rates?
Can the business get an on-demand monthly sales report?

## Technologies Used

### Programming & Data Generation

* Python
* Faker
* PyMySQL

### Database

* MySQL

### SQL Techniques

* SELECT, WHERE, GROUP BY, HAVING
* INNER JOIN and LEFT JOIN
* CASE statements
* Conditional aggregation
* Common Table Expressions (CTEs)
* Window functions
* `LAG()`
* `RANK()` / `DENSE_RANK()`
* Date functions
* Stored procedures
* Indexes

### Presentation

* Microsoft PowerPoint

## Dataset & Data Generation

The project uses synthetic e-commerce data generated using Python and the Faker library.

The `seed_data.py` script generates and loads approximately:

* 3,000 customers
* 100 suppliers
* 400 products
* 25,000 orders
* 1–5 items per order
* Approximately 6% returns
* Data spanning roughly two years

The generated data includes realistic customer names, emails, phone numbers, cities, states, products, categories, orders, payments, and return information.

A fixed random seed is used to make the data generation reproducible.

### Data Generation Flow


Python + Faker
      ↓
Synthetic E-commerce Data
      ↓
  PyMySQL
      ↓
MySQL Database
      ↓
SQL Analysis


To generate the data
pip install -r requirements.txt

Then configure the MySQL connection details in 'seed_data.py' and run:
python seed_data.py

## Database Schema

The database consists of 7 interconnected tables:

| Table         | Purpose                                                          |
| ------------- | ---------------------------------------------------------------- |
| 'customers'   | Stores customer information and signup details                   |
| 'suppliers'   | Stores supplier information                                      |
| 'products'    | Stores product, category, pricing, and supplier details          |
| 'orders'      | Stores customer orders and order status                          |
| 'order_items' | Stores products and quantities within each order                 |
| 'payments'    | Stores payment method, status, and transaction amount            |
| 'returns'     | Stores returned items, return reasons, dates, and refund amounts |

### Key Relationships

* Customers → Orders: One-to-Many
* Suppliers → Products: One-to-Many
* Products → Order Items: One-to-Many
* Orders → Order Items: One-to-Many
* Orders → Payments: One-to-One
* Order Items → Returns: One-to-Many

The database design uses primary keys and foreign keys to maintain relationships between the tables.

## SQL Analysis

The analysis is organized around six business questions.

### 1. Revenue Trend Analysis

**Business Question:** Is revenue growing or declining month over month?

**SQL Techniques:**

* CTE
* 'LAG()'
* Date functions
* Percentage calculations

### 2. Customer Segmentation

**Business Question:** Which customers are VIP, regular, or at risk of churn?

**SQL Techniques:**

* 'CASE'
* 'DATEDIFF'
* Aggregation
* Customer-level metrics

### 3. Product Performance

**Business Question:** What are the top 3 products per category by revenue?

**SQL Techniques:**

* Window functions
* RANK() / DENSE_RANK()
* PARTITION BY
* CTE

### 4. Return Analysis

**Business Question:** Which product categories have the highest return rates?

**SQL Techniques:**

* LEFT JOIN
* Conditional aggregation
* COUNT()
* Percentage calculations

### 5. Payment Analysis

**Business Question:** Which payment methods have the highest failure rates?

**SQL Techniques:**

* CASE
* SUM()
* Conditional aggregation
* GROUP BY

### 6. Monthly Sales Report

**Business Question:** Can the business get an on-demand monthly sales report?

**SQL Techniques:**

* Stored procedure
* Aggregation
* Monthly filtering

## Key Insights

### Revenue

* Revenue remained relatively stable at approximately ₹5.2–5.7 Cr per month.
* No clear sustained growth or decline was observed.

### Customer Analysis

* High-value customers were identified using spending, order frequency, and purchase recency.
* At-risk customers were identified based on their inactivity period.

### Product Analysis

* The top 3 products were identified for each category.
* Revenue was relatively distributed across the top-performing products.

### Return Analysis

* Fashion had the highest return rate at 6.66%.
* Return rates across categories were relatively close, ranging from 5.70% to 6.66%.

### Payment Analysis

* COD had the highest payment failure rate at 8.58%.
* Net Banking had the lowest failure rate at 8.04%.

### Monthly Sales Report

* A stored procedure was created to generate monthly orders, revenue, and return information using a single call.

## Project Structure


ecommerce-sales-analytics-sql/
│
├── schema.sql
├── seed_data.py
├── requirements.txt
└── ecommerce_sales_project_sql_pptx.pptx

The SQL analysis queries and supporting documentation will be organized separately as the project develops.

## Project Presentation

The complete project presentation is available in the repository:

**[E-commerce Sales Analytics Project Presentation](./ecommerce_sales_project_sql_pptx.pptx)**

The presentation covers:

* Project objective
* ER diagram
* Database schema
* Six business questions
* SQL techniques used
* Key findings
* Challenges and learnings
* Overall conclusion

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/sakshithyadav/ecommerce-sales-analytics-sql.git
cd ecommerce-sales-analytics-sql
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Create the MySQL database

Run `schema.sql` in MySQL to create the database and required tables.

### 4. Configure the database connection

Update the MySQL connection details in `seed_data.py`.

### 5. Generate and load the data

```bash
python seed_data.py
```

### 6. Run the SQL analysis

Execute the SQL analysis queries in MySQL to answer the six business questions and generate the required insights.

