from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from database_helper import DatabaseHelper
from kivy.graphics import Color, Line
from kivy.core.window import Window
from kivy.properties import NumericProperty, ObjectProperty
from kivy.metrics import dp


class DynamicLabel(Label):
    height = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(
            width=lambda *x: self.setter('text_size')(self, (self.width, None)),
            texture_size=lambda *x: self.setter('height')(self, self.texture_size[1])
        )
        self.bind(height=self._update_height)
        self.text_size = (self.width, None)
        self.size_hint_y = None
        self.markup = True
        self.halign = 'center'
        self.valign = 'middle'
        self.padding = (10, 10)

    def _update_height(self, instance, value):
        self.height = value
        self.update_borders()

    def update_borders(self):
        self.canvas.after.clear()
        with self.canvas.after:
            Color(0.5, 0, 0.8, 1)
            Line(points=[self.x, self.y,
                        self.right, self.y],
                width=1)
            Line(points=[self.right, self.y,
                        self.right, self.top],
                width=1)

class CustomTable(BoxLayout):
    min_row_height = NumericProperty(dp(40))
    table_grid = ObjectProperty(None)

    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.page = 0
        self.rows_per_page = 20
        self.data = self.load_data()
        self.display_data()

    def load_data(self):
        db = DatabaseHelper()
        data = db.fetch_order_data()
        formatted_data = []
        for order_num, details in data.items():
            items = " , ".join([f"{name} ({qty})" for name, qty in details['items']])
            formatted_data.append((order_num, items, details['client_table_number']))
            formatted_data.sort(key=lambda x: x[0], reverse=True)
        return formatted_data

    def update_borders(self, instance, value):
        instance.canvas.after.clear()
        with instance.canvas.after:
            Color(0.5, 0, 0.8, 1)
            Line(points=[instance.x, instance.y,
                        instance.right, instance.y],
                width=1)
            Line(points=[instance.right, instance.y,
                        instance.right, instance.top],
                width=1)

    def create_row_layout(self):
        row = BoxLayout(size_hint_y=None, spacing=1)
        row.bind(minimum_height=row.setter('height'))
        return row

    def display_data(self):
        table_grid = self.ids.table_grid
        table_grid.clear_widgets()
        table_grid.bind(minimum_height=table_grid.setter('height'))
        
        # Calculate available widths
        total_width = Window.width - dp(20)  # Accounting for padding
        order_width = total_width * 0.2      # 1/5 of width
        items_width = total_width * 0.6      # 3/5 of width
        table_width = total_width * 0.2      # 1/5 of width
        
        start_idx = self.page * self.rows_per_page
        end_idx = start_idx + self.rows_per_page
        page_data = self.data[start_idx:end_idx]
        
        for order_number, items, table_number in page_data:
            row = self.create_row_layout()
            
            # Create labels with text wrapping and center alignment
            order_label = DynamicLabel(
                text=str(order_number),
                size_hint_x=1/5,
                color=(0, 0.7, 0.7, 1)
            )
            
            items_label = DynamicLabel(
                text=items,
                size_hint_x=3/5,
                color=(0, 0, 0, 1)
            )
            
            table_label = DynamicLabel(
                text=str(table_number),
                size_hint_x=1/5,
                color=(0, 0, 0.44, 1)
            )
            
            # Set minimum heights
            order_label.height = max(self.min_row_height, order_label.texture_size[1])
            items_label.height = max(self.min_row_height, items_label.texture_size[1])
            table_label.height = max(self.min_row_height, table_label.texture_size[1])
            
            # Make all labels in the row the same height (use maximum height)
            max_height = max(order_label.height, items_label.height, table_label.height)
            order_label.height = max_height
            items_label.height = max_height
            table_label.height = max_height
            
            # Add borders
            self.add_borders(order_label)
            self.add_borders(items_label)
            self.add_borders(table_label)
            
            # Add labels to row
            row.add_widget(order_label)
            row.add_widget(items_label)
            row.add_widget(table_label)
            
            # Add row to grid
            table_grid.add_widget(row)

    def add_borders(self, widget):
        with widget.canvas.after:
            Color(0, 0, 0.8, 1)
            Line(points=[widget.x, widget.y,
                        widget.right, widget.y],
                width=1)
            Line(points=[widget.right, widget.y,
                        widget.right, widget.top],
                width=1)
        widget.bind(size=self.update_borders, pos=self.update_borders)

    def load_next_page(self):
        if (self.page + 1) * self.rows_per_page < len(self.data):
            self.page += 1
            self.display_data()

    def load_previous_page(self):
        if self.page > 0:
            self.page -= 1
            self.display_data()


class TableApp(App):
    def build(self):
        Builder.load_file('table_view.kv')
        return CustomTable()

if __name__ == '__main__':
    TableApp().run()