import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("ice_cream_store.db")
cursor = conn.cursor()

# Create the products table
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (  -- Change 'product' to 'products'
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    product_price REAL NOT NULL
)
''') 

# Create the orders table
cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    daily_order_number INTEGER DEFAULT 0,
    client_table_number INTEGER NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Create the order_items table
cursor.execute('''
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)
''')

# Commit changes and close the connection
conn.commit()
conn.close()
print("Database with products, orders, and order_items tables created successfully.")
