# db.py

import mysql.connector

def get_connection():
    # Replace with your actual credentials!
    return mysql.connector.connect(
        host="localhost",
        user="root",            # most common default user is 'root'
        password="kartheek",# type your own MySQL root/user password here
        database="cafe_billing"
    )

def fetch_menu_items():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, category FROM MenuItem")
    items = cursor.fetchall()
    conn.close()
    return items


def add_menu_item(name, price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO MenuItem (name, price) VALUES (%s, %s)",
        (name, price)
    )
    conn.commit()
    conn.close()

def add_order(item_id, quantity):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Orders (item_id, quantity) VALUES (%s, %s)",
        (item_id, quantity)
    )
    conn.commit()
    conn.close()

# For a test run (optional):
if __name__ == "__main__":
    print(fetch_menu_items())
