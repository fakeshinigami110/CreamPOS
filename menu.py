from kivy.uix.accordion import ObjectProperty
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from database_helper import DatabaseHelper
from kivy.core.window import Window
import random
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import Screen


Builder.load_file("productlist.kv")
from kivy.uix.modalview import ModalView
from kivy.uix.image import Image
from kivy.uix.switch import Switch

class ProductManagerModal(ModalView):
    products = ListProperty([])

    def __init__(self, callback=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.8, 0.8)
        self.edit_mode = False
        self.callback = callback
        self.load_products()

    def load_products(self):
        db = DatabaseHelper()
        self.products = [{'id': p[0], 'name': p[1], 'price': p[2]} for p in db.fetch_products()]
        self.update_view()

    def update_view(self):
        self.ids.product_box.clear_widgets()
        for product in self.products:
            product_row = BoxLayout(size_hint_y=None, height=40)
            
            # Create TextInputs without custom id
            name_input = TextInput(
                text=str(product['name']), 
                multiline=False, 
                readonly=not self.edit_mode
            )
            price_input = TextInput(
                text=str(product['price']), 
                multiline=False, 
                readonly=not self.edit_mode
            )
            
            # Use lambda with default arguments to properly capture product id
            if self.edit_mode:
                name_input.bind(
                    on_text_validate=lambda instance, pid=product['id']: 
                        self.save_product_changes(pid, instance.text, None)
                )
                price_input.bind(
                    on_text_validate=lambda instance, pid=product['id']: 
                        self.save_product_changes(pid, None, instance.text)
                )
            
            product_row.add_widget(name_input)
            product_row.add_widget(price_input)

            if self.edit_mode:
                delete_button = Button(
                    text="Delete", 
                    size_hint_x=0.2, 
                    on_press=lambda x, prod=product: self.delete_product(prod)
                )
                product_row.add_widget(delete_button)
            
            self.ids.product_box.add_widget(product_row)

    def save_product_changes(self, product_id, new_name=None, new_price=None):
        db = DatabaseHelper()
        try:
            if new_price is not None:
                new_price = float(new_price)
            db.edit_product(product_id, new_name, new_price)
            self.load_products()
            if self.callback:
                self.callback()
        except ValueError as e:
            print(f"Error saving changes: {e}")

    def toggle_edit_mode(self, instance, value):
        self.edit_mode = value
        self.update_view()

    def delete_product(self, product):
        db = DatabaseHelper()
        db.delete_product(product_id=product['id'])
        self.load_products()
        if self.callback:
            self.callback()

    def add_product(self, name, price):
        if name.strip() and price.strip():
            try:
                db = DatabaseHelper()
                db.add_product(name, float(price))
                self.load_products()
                self.ids.new_product_name.text = ""
                self.ids.new_product_price.text = ""
                if self.callback:
                    self.callback()
            except ValueError as e:
                print(f"Error adding product: {e}")


class ProductRow(BoxLayout):
    product_name = StringProperty("")
    product_price = StringProperty("")
    quantity_input = StringProperty("0")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._bind_input, 0)
        
    

    def _bind_input(self, dt):
        self.ids.input_box.bind(text=self.on_quantity_change)

    def on_quantity_change(self, instance, value):
        rv = None
        current_widget = self
        
        while current_widget:
            if isinstance(current_widget, RecycleView):
                rv = current_widget
                break
            current_widget = current_widget.parent
            
        if rv:
            try:
                index = rv.data.index({'product_name': self.product_name, 
                                    'product_price': self.product_price, 
                                    'quantity_input': self.quantity_input})
                
                if value.strip() == "" or value.isdigit():
                    new_value = value if value.strip() != "" else "0"
                    rv.data[index]['quantity_input'] = new_value
                    self.quantity_input = new_value
                    print(f"Updated quantity for {self.product_name}: {new_value}")
            except ValueError:
                print(f"Could not find product {self.product_name} in RecycleView data")
        else:
            print("Could not find RecycleView in widget hierarchy")

class ProductListView(RecycleView):
    products = ListProperty([])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(size=self.on_window_size)
        self.calculate_items_per_page()
        self.page = 0
        
    def load_products(self):
        db = DatabaseHelper()
        self.products = db.fetch_products()
        self.update_view()

    def update_view(self):
        start_idx = self.page * self.items_per_page
        end_idx = start_idx + self.items_per_page
        display_products = self.products[start_idx:end_idx]

        # Create new data with reset quantities
        self.data = [
            {"product_name": product[1], 
             "product_price": f"${product[2]:.2f}", 
             "quantity_input": "0"}
            for product in display_products
        ]
        # Force a refresh of the view
        self.refresh_from_data()
        print("Updated view with data:", self.data)

    def calculate_items_per_page(self):
        window_height = Window.height
        item_height = 10
        available_height = window_height - 100
        numbers = int(available_height / item_height)
        numbers = numbers % 4
        numbers = 4 - numbers 
        self.items_per_page = int(available_height / item_height) + numbers

    def on_window_size(self, window, size):
        self.calculate_items_per_page()
        self.update_view()

    def reset_quantities(self):
        # Reset quantities in the data
        for item in self.data:
            item['quantity_input'] = "0"
        # Force a refresh of the view
        self.refresh_from_data()

    def next_page(self):
        if (self.page + 1) * self.items_per_page < len(self.products):
            self.page += 1
            self.update_view()

    def prev_page(self):
        if self.page > 0:
            self.page -= 1
            self.update_view()

class ProductSelectionScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.product_list = ProductListView(size_hint_y=6)
        self.add_widget(self.product_list)
        
        pagination_layout = GridLayout(cols=3, size_hint_y=0.2)
        pagination_layout.add_widget(Button(text="Previous", on_press=lambda x: self.product_list.prev_page()))
        pagination_layout.add_widget(Button(text="Next", on_press=lambda x: self.product_list.next_page()))
        confirm_button = Button(text="Confirm Order", size_hint_y=0.1, on_press=self.confirm_order)
        pagination_layout.add_widget(confirm_button)
        self.add_widget(pagination_layout)

        self.product_list.load_products()
        
    def open_product_manager(self):
        product_manager = ProductManagerModal(callback=self.refresh_products)
        product_manager.open()

    def refresh_products(self):
        self.product_list.load_products()
    def confirm_order(self, instance):
        print("Current data in RecycleView:", self.product_list.data)
        
        db = DatabaseHelper()
        order_id = db.add_order(
            daily_order_number=random.randint(1, 100), 
            client_table_number=random.randint(1, 10)
        )

        start_idx = self.product_list.page * self.product_list.items_per_page
        visible_products = self.product_list.products[start_idx:start_idx + self.product_list.items_per_page]

        for i, product in enumerate(visible_products):
            try:
                quantity = int(self.product_list.data[i]["quantity_input"])
                if quantity > 0:
                    product_id = product[0]
                    db.add_order_item(order_id, product_id, quantity)
                    print(f"Added {quantity} of product {product[1]} to order")
            except (ValueError, IndexError) as e:
                print(f"Error processing product {product[1]}: {e}")
                continue

        # Reset quantities and update the view
        self.product_list.reset_quantities()
        self.show_confirmation_popup()
        print("Order confirmed and added to the database.")
    
    def show_confirmation_popup(self):
        popup = Popup(title='Order Confirmed',
                     content=Label(text='Your order has been confirmed!'),
                     size_hint=(None, None), size=(400, 200))
        popup.open()

class IceCreamApp(App):
    def build(self):
        Window.enable_vkeyboard = False
        return ProductSelectionScreen()

if __name__ == "__main__":
    IceCreamApp().run()