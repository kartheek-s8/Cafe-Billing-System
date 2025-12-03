# main.py - Simple console Cafe Billing System
import db
import orders
import billing

def display_menu(menu_items):
    print("\n========== CAFE MENU ==========")
    print(f"{'ID':<5} {'Item':<25} {'Price (₹)':>10}")
    print("-" * 45)
    for item_id, name, price, category in menu_items:
        print(f"{item_id:<5} {name:<25} {price:>10.2f}")
    print("-" * 45)

def take_order(menu_items):
    print("\nEnter item IDs and quantities.")
    print("Type 0 when you are done.\n")

    valid_ids = {item[0] for item in menu_items}
    order_items = []  # list of (item_id, quantity)

    while True:
        try:
            item_id = int(input("Enter item ID (0 to finish): "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if item_id == 0:
            break

        if item_id not in valid_ids:
            print("Invalid item ID. Please try again.")
            continue

        try:
            qty = int(input("Enter quantity: "))
        except ValueError:
            print("Please enter a valid quantity.")
            continue

        if qty <= 0:
            print("Quantity must be greater than 0.")
            continue

        order_items.append((item_id, qty))
        print("Item added to order.\n")

    if not order_items:
        print("No items in order.")
    return order_items

def print_bill(bill_data):
    print("\n========== BILL ==========")
    print(f"{'Item':<25} {'Qty':>3} {'Price':>10} {'Total':>10}")
    print("-" * 55)

    for item in bill_data['items']:
        name = item['name']
        qty = item['quantity']
        price = item['price']
        total = item['total']
        print(f"{name:<25} {qty:>3} {price:>10.2f} {total:>10.2f}")

    print("-" * 55)
    print(f"{'Subtotal':<25} {'':>3} {'':>10} {bill_data['subtotal']:>10.2f}")
    print(f"{'GST (5%)':<25} {'':>3} {'':>10} {bill_data['gst_amount']:>10.2f}")
    print("=" * 55)
    print(f"{'GRAND TOTAL':<25} {'':>3} {'':>10} {bill_data['grand_total']:>10.2f}")
    print("=" * 55)
    print("Thank you for visiting the cafe!\n")

def main():
    while True:
        print("\n====== CAFE BILLING SYSTEM ======")
        print("1. Show menu and take order")
        print("2. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            menu_items = db.fetch_menu_items()
            if not menu_items:
                print("No menu items found in database.")
                continue

            display_menu(menu_items)
            order_items = take_order(menu_items)

            if not order_items:
                continue  # back to main menu

            # Create order in DB and calculate bill
            order_id, total = orders.create_order(order_items)
            bill_data = billing.calculate_bill(order_items)

            print_bill(bill_data)

        elif choice == "2":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
