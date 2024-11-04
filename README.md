# Simple Demo POS App

An interactive Kivy-based app for managing and ordering products, designed to be used in a point-of-sale or inventory management context. The app provides a user-friendly interface for viewing products, managing orders, and tracking order details.

## Features

- **Product Management**: 
  - View, edit, add, and delete products in the database.
  - Easily toggle edit mode to update product details.

- **Order Management**:
  - Browse available products with pagination.
  - Add items to orders with specified quantities.
  - Confirm and store orders, with automatic resets after each transaction.
  - View detailed order history with itemized breakdowns.

- **Responsive UI**:
  - The interface adjusts to different screen sizes for optimal user experience.
  - Pagination for products and orders, ensuring easy navigation.

## Components

- **menu.py**: Main screen handling product management and ordering interface.
- **order_screen.py**: Displays order history in a tabular format with dynamic layout adjustments.
- **DatabaseHelper**: Helper class for database operations (CRUD for products and orders).

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/IceCreamApp.git
   ```
2. Navigate to the project directory:
    ```bash
    cd CreamPos
    ```
3. Install required dependencies:
    ```bash
    pip install kivy
    ```
4. run the application
    ```bash
    python menu.py
    ```
    or
    ```bash
    python order_screen.py
    ```

# Usage
- ###  **Product Management:**

    - Click on the `Edit Mode` switch to modify products.
    
    - Add new products with the "Add Product" button.
- ### Placing Orders:

    - Select quantities for each product.
    - Confirm the order using the "Confirm Order" button.
- ### Order History:

    - Check past orders with product details, including quantities and table numbers.
### Project Structure
- `menu.py`: Contains the main UI for product management and order placement.
- `order_screen.py`: Handles order history display.
- `database_helper.py`: Database interactions and helper functions.
