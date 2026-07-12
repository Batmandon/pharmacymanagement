from database import get_cursor
from  services.JWT import decode_token
from routes.auth import get_user


def expiry_products(token):
    payload = decode_token(token)
    email = payload.get("sub")

    with get_cursor() as cursor:
        user = get_user(cursor, email)

        if not user:
            return {"error": "user not found"}

        user_id = user["id"]

        cursor.execute("""
            SELECT id, expiry_date,
                   (expiry_date - CURRENT_DATE) AS days_left
            FROM products
            WHERE user_id = %s
        """, (user_id,))

        data = cursor.fetchall()

        if not data:
            return {"message": "no products found"}

        for row in data:
            expiry_date = row["expiry_date"]
            days_left = row["days_left"]

            if expiry_date is None:
                status = "expiry date not set"
            elif days_left is None:
                status = "expiry date not set"
            elif days_left < 0:
                status = "expired"
            elif days_left == 0:
                status = "expires today"
            elif days_left <= 30:
                status = f"product expiring in {days_left} days"
            else:
                status = "safe"

            cursor.execute(
                "UPDATE products SET expiry_status = %s WHERE id = %s",
                (status, row["id"])
            )

        return {"message": "expiry statuses updated"}