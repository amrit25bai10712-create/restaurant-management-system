import uuid
from datetime import datetime

class MenuItem:
    def __init__(self, item_id:int, name:str, price:float, category:str):
        self.item_id = item_id
        self.name = name
        self.price = float(price)
        self.category = category

    def __repr__(self):
        return f"MenuItem({self.item_id}, {self.name}, {self.price:.2f}, {self.category})"

class Order:
    def __init__(self, table_number:int):
        self.order_id = str(uuid.uuid4())[:8]
        self.table_number = int(table_number)
        self.items = {}  # item_id -> qty
        self.timestamp = datetime.now()
        self.status = "PENDING"

    def add_item(self, item_id:int, qty:int=1):
        if qty <= 0:
            raise ValueError("Quantity must be positive")
        self.items[item_id] = self.items.get(item_id, 0) + int(qty)

    def subtotal(self, menu:dict):
        total = 0.0
        for iid, qty in self.items.items():
            item = menu.get(iid)
            if item is None:
                raise KeyError(f"Menu item {iid} not found")
            total += item.price * qty
        return total

    def __repr__(self):
        return f"Order({self.order_id}, Table {self.table_number}, status={self.status})"
