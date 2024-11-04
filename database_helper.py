import sqlite3
import random
class DatabaseHelper:
    def __init__(self, db_name="ice_cream_store.db"):
        self.db_name = db_name

    def connect(self):
        """Establishes a database connection and returns the cursor."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def close(self):
        """Commits changes and closes the connection."""
        self.conn.commit()
        self.conn.close()

    def fetch_products(self):
        """Fetches all products from the products table."""
        self.connect()
        self.cursor.execute("SELECT * FROM products")
        products = self.cursor.fetchall()
        self.close()
        return products
    
    def fetch_order_items(self):
        """Fetches all orders from the order items table."""
        self.connect()
        self.cursor.execute("SELECT * FROM order_items")
        products = self.cursor.fetchall()
        self.close()
        return products

    def add_product(self, product_name, product_price):
        """Adds a new product to the products table."""
        self.connect()
        self.cursor.execute(
            "INSERT INTO products (product_name, product_price) VALUES (?, ?)",
            (product_name, product_price)
        )
        self.close()
        print(f"Product '{product_name}' added successfully.")

    def edit_product(self, product_id, new_name=None, new_price=None):
        """Edits an existing product's name or price in the products table."""
        self.connect()
        if new_name:
            self.cursor.execute(
                "UPDATE products SET product_name = ? WHERE product_id = ?",
                (new_name, product_id)
            )
        if new_price is not None:  # allows updating price to 0 if needed
            self.cursor.execute(
                "UPDATE products SET product_price = ? WHERE product_id = ?",
                (new_price, product_id)
            )
        self.close()
        print(f"Product ID '{product_id}' updated successfully.")

    def delete_product(self, product_id):
        """Deletes a product from the products table by its ID."""
        self.connect()
        self.cursor.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
        self.close()
        print(f"Product ID '{product_id}' deleted successfully.")

    def add_order(self, daily_order_number, client_table_number):
        """Inserts a new order in the orders table."""
        self.connect()
        self.cursor.execute(
            "INSERT INTO orders (daily_order_number, client_table_number) VALUES (?, ?)",
            (daily_order_number, client_table_number)
        )
        order_id = self.cursor.lastrowid
        self.close()
        return order_id

    def add_order_item(self, order_id, product_id, quantity):
        """Inserts a new item into the order_items table."""
        self.connect()
        self.cursor.execute(
            "INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)",
            (order_id, product_id, quantity)
        )
        self.close()
        
    def fetch_order_data(self):
        self.connect()
        
        # Query to get order details
        query = '''
        SELECT 
            orders.daily_order_number,
            products.product_name,
            order_items.quantity,
            orders.client_table_number
        FROM 
            orders
        JOIN order_items ON orders.order_id = order_items.order_id
        JOIN products ON order_items.product_id = products.product_id
        ORDER BY orders.daily_order_number
        '''
        
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.close()
        
        # Format data into a structured dictionary (e.g., per daily order)
        formatted_data = {}
        for row in data:
            daily_order_num = row[0]
            product_name = row[1]
            quantity = row[2]
            client_table_num = row[3]
            
            if daily_order_num not in formatted_data:
                formatted_data[daily_order_num] = {
                    'client_table_number': client_table_num,
                    'items': []
                }
            formatted_data[daily_order_num]['items'].append((product_name, quantity))
        
        return formatted_data

# Testing the new methods
# if __name__ == "__main__":
#     db = DatabaseHelper()

#     # Test adding a product
#     # db.add_product("Vanilla Ice Cream", 2.50)
#     # for _ in range(50):
#     #     db.add_product(product_name=f"product{_}",product_price=random.randint(1500 , 20000))
#     # Test editing a product's name and price
#     # db.edit_product(product_id=1, new_name="Chocolate Ice Cream", new_price=3.00)

#     # Test deleting a product
#     # db.delete_product(product_id=1)

#     # Test fetching products
#     # print("All Products:", db.fetch_order_items())
#     print (db.fetch_order_data())