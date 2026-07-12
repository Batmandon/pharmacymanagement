from models.model import AddProduct, UpdateProduct
from database import get_cursor
from  services.JWT import decode_token
from routes.auth import get_user

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Helper Function~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_product(id: int):
    with get_cursor() as cursor: 
        cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
        product = cursor.fetchone()
        return product
    
def get_current_user(token: str):
    payload = decode_token(token)
    
    # Check if decode_token returned an error
    if "error" in payload:
        return payload
    
    email = payload.get("sub")

    with get_cursor() as cursor:
        user = get_user(cursor, email)

    if not user:
        return {"error": "User not found"}

    return user

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Operations~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def add_product(create_product: list[AddProduct] , token: str):
    user = get_current_user(token)
    
    # Check for errors
    if "error" in user:
        return user
    
    for product in create_product:
        with get_cursor() as cursor:
            cursor.execute("INSERT INTO products (user_id, medicine_name, batch_no, expiry_date, price, quantity) VALUES (%s, %s, %s, %s, %s, %s)", 
                       (user["id"], product.medicine_name, product.batch_no, product.expiry_date, product.price, product.quantity))
    
    return {"Product added successfully"}

def edit_product(edit_product: UpdateProduct, product_id:int,  token: str):
    user = get_current_user(token)

    if "error" in user:
        return user
        
    
    with get_cursor() as cursor:
        cursor.execute(
        "UPDATE products SET medicine_name = %s, batch_no = %s, expiry_date = %s, quantity = %s, price = %s WHERE id = %s",
        (edit_product.medicine_name, edit_product.batch_no, edit_product.expiry_date, edit_product.quantity, edit_product.price, product_id)
    )
    return {"Product edited successfully"}
    
def delete_product(product_id: int, token:str):

    payload = decode_token(token)
    email = payload.get("sub")

    with get_cursor() as cursor:
        user = get_user(cursor, email)
        product = get_product(product_id)

        if not user:
            return {"error": "user not found"}
        
        if not product:
            return {"error": "product not found"}
        
        cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))

    return {"Product deleted Successfully"}

def get_product(token: str):
    payload = decode_token(token)
    email = payload.get("sub")

    with get_cursor() as cursor:
        user = get_user(cursor, email)

        if not user:
            return {"error": "user not found"}
        user_id = user["id"]
        
        cursor.execute("SELECT * FROM products WHERE user_id = %s",
                       (user_id,))
        products = cursor.fetchall()
        return products

def get_product_by_name(name: str, token: str):
    name = name.strip()
    payload = decode_token(token)
    email = payload.get("sub")

    with get_cursor() as cursor:
        user = get_user(cursor, email)

        if not user:
            return {"error": "user not found"}
        
        cursor.execute("SELECT * FROM products WHERE name = %s",
                       (name,))
        product = cursor.fetchone()
        return product
