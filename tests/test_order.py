from models import MenuItem, Order

def test_subtotal():
    menu = {1: MenuItem(1,'Burger',60.0,'Mains'), 2: MenuItem(2,'Fries',40.0,'Sides')}
    o = Order(table_number=3)
    o.add_item(1,2)
    o.add_item(2,1)
    assert o.subtotal(menu) == 160.0
