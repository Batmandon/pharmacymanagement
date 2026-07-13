from models.model import UserSignUp, UserSignIn, UserRefresh
from database import get_cursor
from utils.utils import hash_password, verify_password
from services.JWT import create_access_token, create_refresh_token, decode_token
from fastapi import Response, Request, HTTPException, Request

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Helperfunction~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_user(cursor, email: str):
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    return cursor.fetchone()

def get_token_from_cookies(request: Request):
    """Extract token from cookies - use as dependency"""
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return token

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~Auth Operations~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def create_account(sign: UserSignUp):
    with get_cursor() as cursor:

        if get_user(cursor, sign.email):
            return {"error": "Account alrady exists"}
        
        hashed_password= hash_password(sign.password)

        cursor.execute("INSERT INTO users (name, pharmacy_name, email, password)  VALUES (%s, %s, %s, %s)", (sign.name, sign.pharmacy_name ,sign.email, hashed_password))

        return {"Message": "Account Successfully Created"}
    
def login_user(userlogin: UserSignIn, response: Response):
    with get_cursor() as cursor: 
        user =  get_user(cursor, userlogin.email)

        if not user or not verify_password(userlogin.password, user["password"]):
            return {"error": "Invalid email or password"}
        
        token_data = {"sub": user["email"], "name": user["name"]}

        access_token = create_access_token(token_data)
        refresh_token =  create_refresh_token(token_data)

        response.set_cookie(
            key = "access_token",
            value = access_token,
            httponly = True,
            secure = True, # True for production false for local
            samesite = "none", # none for production lax for local
            domain = "127.0.0.1",
            max_age = 1800
        )
        response.set_cookie(
            key = "refresh_token",
            value = refresh_token,
            httponly = True,
            secure = True,
            samesite = "none",
            domain = "127.0.0.1",
            max_age = 604800
        )
    
        return {"message": "Login successful", "name": user["name"]}


def get_user_info_from_request(request: Request):
    token = request.cookies.get("access_token")
    
    if not token:
        return {"error": "Not authenticated"}
    
    payload = decode_token(token)
    
    if "error" in payload:
        return payload
    
    return {
        "email": payload.get("sub"),
        "name": payload.get("name")
    }

def get_user_info_refresh_token (request: Request, response: Response):
    token = request.cookies.get("refresh_token")

    if not token:
        return{"error": "Please Log IN"}
    
    payload = decode_token(token)

    if "error" in payload:
        return payload
    
    email = payload.get("sub")
    with get_cursor() as cursor:
        user = get_user(cursor, email)

        if not user:
            return {"error": "user not found"}
    
    access_token =  create_access_token({
        "sub": user["email"],
        "name": user["name"]
    })

    response.set_cookie(
        key = "access_token",
        value = access_token,
        httponly = True,
        secure = True,
        samesite = "none",
        max_age = 1800
    
    )

def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="none",
        secure=True
    )

    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        samesite="none",
        secure=True
    )
    return {"message": "Logged out successfully"}
