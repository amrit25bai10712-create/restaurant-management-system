from system import RestaurantSystem
import sys

def input_int(prompt):
    while True:
        v = input(prompt).strip()
        if v.isdigit():
            return int(v)
        print("Please enter a valid integer.")

def run_system():
    rs = RestaurantSystem()
    while True:
        print("\n==== Restaurant RMS ====")
        print("1. View Menu")
        print("2. Place New Order")
        print("3. View/Update Active Orders")
        print("4. Close Order and Print Bill")
        print("5. Exit")
        choice = input("Choose an option: ").strip()
        if choice == '1':
            print(rs.display_menu())
        elif choice == '2':
            table = input_int("Enter table number: ")
            items = {}
            print("Enter Item ID and Quantity (e.g., '1 2'), or 'done' to finish:")
            while True:
                line = input("Item and qty: ").strip()
                if line.lower() == 'done':
                    break
                parts = line.split()
                if len(parts) != 2 or not parts[0].isdigit() or not parts[1].isdigit():
                    print("Invalid format. Use: ID qty")
                    continue
                iid = int(parts[0])
                qty = int(parts[1])
                items[iid] = items.get(iid, 0) + qty
                item = rs.menu.get(iid)
                if item:
                    print(f"Added {qty} x {item.name} to the order.")
                else:
                    print("Warning: item id not found (will error on finalize).")

            try:
                order = rs.place_order(table, items)
                est = order.subtotal(rs.menu)
                print(f"\n✅ Order #{order.order_id} placed successfully! Estimated Total: ₹{est:.2f}")
            except Exception as e:
                print(f"Error placing order: {e}")

        elif choice == '3':
            active = rs.list_active_orders()
            if not active:
                print("No active orders.")
            else:
                for o in active:
                    print(f"ID: {o.order_id} | Table: {o.table_number} | Status: {o.status} | Time: {o.timestamp}")
                oid = input("Enter Order ID to update status, or press Enter to go back: ").strip()
                if oid:
                    print("Set status to: PENDING, PREPARING, COMPLETE")
                    ns = input("New status: ").strip().upper()
                    try:
                        rs.update_order_status(oid, ns)
                        print("Status updated.")
                    except Exception as e:
                        print(f"Error: {e}")

        elif choice == '4':
            active = rs.list_active_orders()
            if not active:
                print("No active orders to close.")
            else:
                for o in active:
                    print(f"ID: {o.order_id} | Table: {o.table_number} | Status: {o.status}")
                oid = input("Enter Order ID to close and bill: ").strip()
                try:
                    res = rs.calculate_and_close_bill(oid)
                    print(res['receipt'])
                except Exception as e:
                    print(f"Error: {e}")

        elif choice == '5':
            print("Exiting. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    run_system()
