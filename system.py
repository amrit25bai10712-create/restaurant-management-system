from models import MenuItem, Order
from datetime import datetime

TAX_RATE = 0.08

class RestaurantSystem:
    def __init__(self):
        self.menu = {}
        self.active_orders = []
        self._initialize_menu()

    def _initialize_menu(self):
        # Hardcoded sample menu. Modify as needed.
        items = [
            (1, "Classic Burger", 60.0, "Mains"),
            (2, "Veg Burger", 55.0, "Mains"),
            (3, "Fries", 40.0, "Sides"),
            (4, "Garlic Bread", 50.0, "Starters"),
            (5, "Cold Coffee", 80.0, "Beverages"),
            (6, "Chocolate Shake", 90.0, "Beverages"),
            (7, "Ice Cream Scoop", 45.0, "Desserts"),
        ]
        for iid, name, price, cat in items:
            self.menu[iid] = MenuItem(iid, name, price, cat)

    def display_menu(self):
        # Group by category
        cats = {}
        for item in self.menu.values():
            cats.setdefault(item.category, []).append(item)
        lines = []
        for cat in sorted(cats):
            lines.append(f"\n== {cat} ==")
            for it in sorted(cats[cat], key=lambda x: x.item_id):
                lines.append(f"{str(it.item_id).zfill(2)}. {it.name} — ₹{it.price:.2f}")
        return "\n".join(lines)

    def place_order(self, table_number:int, items:dict):
        o = Order(table_number)
        for iid, qty in items.items():
            if iid not in self.menu:
                raise KeyError(f"Menu item {iid} not found")
            o.add_item(iid, qty)
        self.active_orders.append(o)
        return o

    def list_active_orders(self):
        return list(self.active_orders)

    def find_order(self, order_id):
        for o in self.active_orders:
            if o.order_id == order_id:
                return o
        return None

    def update_order_status(self, order_id, new_status):
        o = self.find_order(order_id)
        if not o:
            raise KeyError("Order not found")
        allowed = ["PENDING","PREPARING","COMPLETE"]
        if new_status not in allowed:
            raise ValueError("Invalid status")
        o.status = new_status
        return o

    def calculate_and_close_bill(self, order_id):
        o = self.find_order(order_id)
        if not o:
            raise KeyError("Order not found")
        subtotal = o.subtotal(self.menu)
        tax = round(subtotal * TAX_RATE, 2)
        final = round(subtotal + tax, 2)
        receipt = self._format_receipt(o, subtotal, tax, final)
        self.active_orders.remove(o)
        return {"receipt": receipt, "subtotal": subtotal, "tax": tax, "final": final}

    def _format_receipt(self, order, subtotal, tax, final):
        lines = []
        lines.append("\n----- Receipt -----")
        lines.append(f"Order ID: {order.order_id}")
        lines.append(f"Table: {order.table_number}")
        lines.append(f"Date: {order.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("\nItems:")
        for iid, qty in order.items.items():
            item = self.menu.get(iid)
            lines.append(f"{qty} x {item.name} (₹{item.price:.2f}) -> ₹{item.price*qty:.2f}")
        lines.append(f"\nSubtotal: ₹{subtotal:.2f}")
        lines.append(f"Tax (8%): ₹{tax:.2f}")
        lines.append(f"Total: ₹{final:.2f}")
        lines.append("-------------------\n")
        return "\n".join(lines)
