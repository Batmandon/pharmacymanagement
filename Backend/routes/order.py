from database import get_cursor
from  services.JWT import decode_token
from routes.auth import get_user
from models.model import Order
from urllib.parse import quote
import json
# ~~~~~~~~~~~~~~~~~~~~~~~ Helper Function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_order(user_id: int):
    with get_cursor() as cursor:
        cursor.execute("""SELECT orders.id, orders.quantity,orders.status, products.medicine_name, products.quantity AS current_stock
        FROM orders
        JOIN products ON orders.product_id = products.id
        WHERE orders.user_id = %s""", 
                       (user_id,))
        orders = cursor.fetchall()
        return orders


# ~~~~~~~~~~~~~~~~~~~~~~~~ Operation Function ~~~~~~~~~~~~~~~~~~~~~~~~~
def add_order(token: str):

    ORDER_AMOUNT = 20
    payload = decode_token(token)
    email = payload.get("sub")

    with get_cursor() as cursor:
        user = get_user(cursor, email)

        if not user: 
            return {"error": "user not found"}
        
        cursor.execute("""INSERT INTO orders(user_id, product_id, quantity)
                       SELECT %s, products.id, %s FROM products
                       WHERE products.quantity <= 10 AND products.user_id = %s
                       AND NOT EXISTS (
                           SELECT 1 FROM orders 
                           WHERE orders.user_id = %s AND orders.product_id = products.id
                        )
                       """,
                       (user["id"], ORDER_AMOUNT, user["id"], user["id"]))

        return {"message": "ordered added successfully"}

def get_orders(token: str):
    payload = decode_token(token)
    email = payload.get("sub")

    with get_cursor() as cursor:
        user = get_user(cursor, email)

        if not user: 
            return {"error": "user not found"}
        
        user_id = user["id"]
        orders = get_order(user_id)

        return orders
        
def generate_whatapp_url(token: str):
    payload = decode_token(token)
    email = payload.get("sub")

    with get_cursor() as cursor:
        user = get_user(cursor, email)

        if not user: 
            return {"error": "user not found"}
        
        user_id = user["id"]
        pharmacy_name = user["pharmacy_name"]
        orders = get_order(user_id)

    
    items_text = ""

    for order in orders: 
        items_text += f"• {order['medicine_name']} x {order['quantity']}\n"

    text = f"""Order list
Pharmacy: {pharmacy_name}

Items:
{items_text}"""
    
    return f"https://wa.me/?text={quote(text)}"


def log_order(items: list, token: str, confirm_duplicate: bool = False):
    payload = decode_token(token)
    email = payload.get("sub")

    with get_cursor() as cursor:
        user = get_user(cursor, email)

        if not user:
            return {"error": "user not found"}

        user_id = user["id"]

    with get_cursor() as cursor:
        # Step 1: check for duplicate (sequence-independent)
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM orders_log
                WHERE user_id = %(user_id)s
                  AND created_at::date = CURRENT_DATE
                  AND (
                      SELECT jsonb_agg(elem ORDER BY (elem->>'id')::int)
                      FROM jsonb_array_elements(items) elem
                  ) = (
                      SELECT jsonb_agg(elem ORDER BY (elem->>'id')::int)
                      FROM jsonb_array_elements(%(items)s::jsonb) elem
                  )
            ) AS is_duplicate
            """, {"user_id": user_id, "items": json.dumps(items)})

        is_duplicate = cursor.fetchone()["is_duplicate"]

        # Step 2: if duplicate found and user hasn't confirmed yet, warn instead of inserting
        if is_duplicate and not confirm_duplicate:
            return {
                "warning": "duplicate_order",
                "message": "Same order already has been sent today. Confirm to send again?"
            }

        # Step 3: insert (either no duplicate, or user confirmed override)
        cursor.execute("""
            INSERT INTO orders_log (user_id, items)
            VALUES (%s, %s)
            """, (user_id, json.dumps(items)))

    return {"message": "Order logged"}

def get_order_history(token: str):
    payload = decode_token(token)
    email = payload.get("sub")

    with get_cursor() as cursor:
        user = get_user(cursor, email)

        if not user: 
            return {"error": "user not found"}

        user_id = user["id"]

    with get_cursor() as cursor:
        cursor.execute(
            "SELECT * FROM orders_log WHERE user_id = %s ORDER BY created_at DESC",
            (user_id,)
        )
        order_history = cursor.fetchall()

    return order_history

def update_status(status: str, token: str):
    payload = decode_token(token)
    email = payload.get("sub")

    with get_cursor() as cursor:
        user = get_user(cursor, email)

        if not user:
            return {"error": "user not found"}

        user_id = user["id"]

        cursor.execute(
            "UPDATE orders SET status = %s WHERE user_id = %s",
            (status, user_id)
        )

    return {"message": "status updated successfully"}