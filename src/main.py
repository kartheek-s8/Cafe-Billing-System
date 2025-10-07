# main.py - Entry point for Cafe Billing System
import db
import orders
import billing


def display_menu():
    """Display all menu items from database"""
    print("\n" + "=" * 50)
    print("           CAFE MENU")
    print("=" * 50)

    menu_items = db.fetch_menu_items()

    current_category = None
    for item in menu_items:
        item_id, name, price, category = item[0], item[1], item[2], item[3]

        # Print category header
        if category != current_category:
            print(f"\n--- {category} ---")
            current_category = category

        print(f"{item_id}. {name:<35} Rs. {price:.2f}")

    print("=" * 50 + "\n")


def take_order():
    """Take customer order"""
    display_menu()

    order_items = []
    print("Enter items to order (type 'done' when finished):")

    while True:
        item_id = input("\nEnter Item ID (or 'done' to finish): ").strip()

        if item_id.lower() == 'done':
            break

        if not item_id.isdigit():
            print("Please enter a valid item ID!")
            continue

        quantity = input("Enter quantity: ").strip()

        if not quantity.isdigit() or int(quantity) <= 0:
            print("Please enter a valid quantity!")
            continue

        order_items.append((int(item_id), int(quantity)))

    return order_items


def main():
    """Main function"""
    print("\n" + "*" * 50)
    print("      WELCOME TO CAFE BILLING SYSTEM")
    print("*" * 50)

    while True:
        print("\n--- MAIN MENU ---")
        print("1. View Menu")
        print("2. Place New Order")
        print("3. Exit")

        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == '1':
            display_menu()

        elif choice == '2':
            order_list = take_order()

            if not order_list:
                print("\nNo items ordered!")
                continue

            # Process the order
            order_id, total = orders.create_order(order_list)

            # Generate bill
            billing.generate_bill(order_id, order_list)

        elif choice == '3':
            print("\nThank you for visiting! Have a great day!")
            break

        else:
            print("\nInvalid choice! Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
