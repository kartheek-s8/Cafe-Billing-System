# orders.py - Handles order creation and management
import db


def create_order(order_items):
    """
    Create a new order and store it in the database

    Args:
        order_items: List of tuples [(item_id, quantity), ...]

    Returns:
        tuple: (order_id, total_amount)
    """
    conn = db.get_connection()
    cursor = conn.cursor()

    total_amount = 0.0
    order_details = []

    # Calculate total and validate items
    for item_id, quantity in order_items:
        # Fetch item details from database
        cursor.execute(
            "SELECT id, name, price FROM MenuItem WHERE id = %s",
            (item_id,)
        )
        item = cursor.fetchone()

        if not item:
            print(f"Warning: Item ID {item_id} not found in menu!")
            continue

        item_id, item_name, item_price = item[0], item[1], float(item[2])
        subtotal = item_price * quantity
        total_amount += subtotal

        # Store for later insertion
        order_details.append({
            'item_id': item_id,
            'item_name': item_name,
            'price': item_price,
            'quantity': quantity,
            'subtotal': subtotal
        })

    # If no valid items, return None
    if not order_details:
        conn.close()
        return None, 0.0

    # Insert orders into database
    order_id = None
    for detail in order_details:
        cursor.execute(
            "INSERT INTO Orders (item_id, quantity, total_amount) VALUES (%s, %s, %s)",
            (detail['item_id'], detail['quantity'], detail['subtotal'])
        )
        # Get the last inserted order_id
        if order_id is None:
            order_id = cursor.lastrowid

    conn.commit()
    conn.close()

    print(f"\nOrder #{order_id} created successfully!")
    print(f"Total items: {len(order_details)}")

    return order_id, total_amount


def get_order_details(order_id):
    """
    Fetch order details from database

    Args:
        order_id: The order ID to fetch

    Returns:
        list: List of order items with details
    """
    conn = db.get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT o.order_id, m.name, m.price, o.quantity, o.total_amount, o.order_date
        FROM Orders o
        JOIN MenuItem m ON o.item_id = m.id
        WHERE o.order_id = %s
    """, (order_id,))

    results = cursor.fetchall()
    conn.close()

    return results


def display_order_summary(order_items):
    """
    Display a summary of the order before processing

    Args:
        order_items: List of tuples [(item_id, quantity), ...]
    """
    conn = db.get_connection()
    cursor = conn.cursor()

    print("\n" + "=" * 50)
    print("           ORDER SUMMARY")
    print("=" * 50)

    total = 0.0
    print(f"{'Item':<30} {'Qty':<5} {'Price':<10} {'Subtotal':<10}")
    print("-" * 50)

    for item_id, quantity in order_items:
        cursor.execute(
            "SELECT name, price FROM MenuItem WHERE id = %s",
            (item_id,)
        )
        result = cursor.fetchone()

        if result:
            name, price = result[0], float(result[1])
            subtotal = price * quantity
            total += subtotal

            print(f"{name:<30} {quantity:<5} Rs.{price:<8.2f} Rs.{subtotal:<8.2f}")

    print("-" * 50)
    print(f"{'TOTAL':<45} Rs.{total:.2f}")
    print("=" * 50 + "\n")

    conn.close()
    return total
