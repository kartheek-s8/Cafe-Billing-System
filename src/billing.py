# billing.py - Handles billing calculations and receipt generation
import db


def calculate_bill(order_items):
    """
    Calculate the total bill with tax

    Args:
        order_items: List of tuples [(item_id, quantity), ...]

    Returns:
        dict: Dictionary containing bill details
    """
    conn = db.get_connection()
    cursor = conn.cursor()

    subtotal = 0.0
    items_detail = []

    for item_id, quantity in order_items:
        cursor.execute(
            "SELECT name, price FROM MenuItem WHERE id = %s",
            (item_id,)
        )
        result = cursor.fetchone()

        if result:
            name, price = result[0], float(result[1])
            item_total = price * quantity
            subtotal += item_total

            items_detail.append({
                'name': name,
                'price': price,
                'quantity': quantity,
                'total': item_total
            })

    conn.close()

    # Calculate GST (5% for restaurant items in India)
    gst_rate = 0.05
    gst_amount = subtotal * gst_rate
    grand_total = subtotal + gst_amount

    return {
        'items': items_detail,
        'subtotal': subtotal,
        'gst_rate': gst_rate * 100,
        'gst_amount': gst_amount,
        'grand_total': grand_total
    }


def generate_bill(order_id, order_items):
    """
    Generate and display the final bill

    Args:
        order_id: The order ID
        order_items: List of ordered items
    """
    bill_details = calculate_bill(order_items)

    print("\n" + "=" * 60)
    print("                  CAFE - INVOICE")
    print("=" * 60)
    print(f"Order ID: #{order_id}")
    print("=" * 60)

    # Print item details
    print(f"\n{'Item':<35} {'Qty':<5} {'Price':<10} {'Total':<10}")
    print("-" * 60)

    for item in bill_details['items']:
        print(f"{item['name']:<35} {item['quantity']:<5} "
              f"Rs.{item['price']:<8.2f} Rs.{item['total']:<8.2f}")

    print("-" * 60)

    # Print totals
    print(f"{'Subtotal:':<50} Rs.{bill_details['subtotal']:.2f}")
    print(f"{'GST (' + str(bill_details['gst_rate']) + '%):':<50} "
          f"Rs.{bill_details['gst_amount']:.2f}")
    print("=" * 60)
    print(f"{'GRAND TOTAL:':<50} Rs.{bill_details['grand_total']:.2f}")
    print("=" * 60)

    print("\n       Thank you for visiting Cafe!")
    print("              Please visit again! :)")
    print("=" * 60 + "\n")

    return bill_details


def save_receipt(order_id, bill_details):
    """
    Save receipt to a text file (optional feature)

    Args:
        order_id: The order ID
        bill_details: Dictionary with bill information
    """
    filename = f"receipt_{order_id}.txt"

    with open(filename, 'w') as file:
        file.write("=" * 60 + "\n")
        file.write("                  CAFE - INVOICE\n")
        file.write("=" * 60 + "\n")
        file.write(f"Order ID: #{order_id}\n")
        file.write("=" * 60 + "\n\n")

        file.write(f"{'Item':<35} {'Qty':<5} {'Price':<10} {'Total':<10}\n")
        file.write("-" * 60 + "\n")

        for item in bill_details['items']:
            file.write(f"{item['name']:<35} {item['quantity']:<5} "
                       f"Rs.{item['price']:<8.2f} Rs.{item['total']:<8.2f}\n")

        file.write("-" * 60 + "\n")
        file.write(f"{'Subtotal:':<50} Rs.{bill_details['subtotal']:.2f}\n")
        file.write(f"{'GST (' + str(bill_details['gst_rate']) + '%):':<50} "
                   f"Rs.{bill_details['gst_amount']:.2f}\n")
        file.write("=" * 60 + "\n")
        file.write(f"{'GRAND TOTAL:':<50} Rs.{bill_details['grand_total']:.2f}\n")
        file.write("=" * 60 + "\n\n")
        file.write("       Thank you for visiting Cafe!\n")
        file.write("              Please visit again! :)\n")
        file.write("=" * 60 + "\n")

    print(f"Receipt saved as {filename}")
