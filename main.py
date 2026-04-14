import pandas as pd
import sqlite3

conn = sqlite3.connect("data.sqlite")

product_data = pd.read_sql("""
SELECT *
FROM products;
""", conn)

""" ORDER BY """

# ORDER BY productName (defaults to ASC)
product_name = pd.read_sql("""
                           SELECT *
                           FROM products
                           ORDER BY productName;
""", conn)

# ORDER BY description length
descr_length = pd.read_sql("""
                           SELECT *, length(productDescription) AS descr_length
                           FROM products
                           ORDER BY descr_length;
""", conn)

# ORDER BY multiple criteria. in this case, ordering by vendors alphabetically and productname alphabetically, but prioritising vendors
two_criteria = pd.read_sql("""
                           SELECT productVendor, productName, MSRP
                           FROM products
                           ORDER BY productVendor, productName;
""", conn)

# DISTINCT will skip over duplicates. below, we're returning the number of *unique* vendors and product names
distinct_number = pd.read_sql("""
                           SELECT COUNT(DISTINCT productVendor) AS num_vendors,
                                COUNT(DISTINCT productName) as num_product_names
                           FROM products
""", conn)

product_stock = pd.read_sql("""
                           SELECT productname, quantityInStock
                           FROM products
                           ORDER BY CAST(quantityInStock AS INTEGER);
""", conn)

# print(product_data)
# print(product_name)
# print(descr_length)
# print(two_criteria)
# print(distinct_number)
# print(product_stock)

""" LIMIT """

orders = pd.read_sql("""
SELECT *
FROM orders
LIMIT 5;
""", conn)

# LIMIT and ORDER BY combined. ordering by comment length
comment_length = pd.read_sql("""
SELECT *
FROM orders
                     ORDER BY length(comments) DESC
LIMIT 10;
""", conn)

# ordering by comment length but only when the order was cancelled
cancelled_orders = pd.read_sql("""
                               SELECT *
                               FROM orders
                               WHERE status = "Cancelled"
                               ORDER BY length(comments) DESC
                               LIMIT 10;
""", conn)

# multiple statuses
cancelled_resolved_orders = pd.read_sql("""
                               SELECT *
                               FROM orders
                               WHERE status IN ("Cancelled", "Resolved")
                               ORDER BY length(comments) DESC
                               LIMIT 10;
""", conn)

first5_customers = pd.read_sql("""
                               SELECT DISTINCT customerNumber, orderDate
                               FROM orders
                               ORDER BY orderDate
                               LIMIT 5;
""", conn)

# 10 newest orders. not been shipped, not been cancelled
newest_orders = pd.read_sql("""
                            SELECT *
                            FROM orders
                            WHERE shippedDate = ""
                            AND status != "Cancelled"
                            ORDER BY orderDate DESC
                            LIMIT 10;
""", conn)

longest_order = pd.read_sql("""
                            SELECT *, julianday(shippedDate) - julianday(orderDate) AS days_to_fulfill
                            FROM orders
                            WHERE shippedDate != ""
                            ORDER BY days_to_fulfill DESC
                            LIMIT 1;
""", conn)


# print(orders)
# print(comment_length)
# print(cancelled_orders)
# print(cancelled_resolved_orders)
# print(first5_customers)
# print(newest_orders)
# print(longest_order)

conn.close()