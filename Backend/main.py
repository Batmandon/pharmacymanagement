from typing import Any
from fastapi import FastAPI, HTTPException,Depends, Request, Response, Body
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import create_account, login_user, get_user_info_from_request, get_token_from_cookies, get_user_info_refresh_token, logout
from database import Create_database
from models.model import UserSignIn, UserSignUp, UserRefresh, AddProduct, UpdateProduct, Order
from routes.prodcrud import add_product, edit_product, delete_product, get_product, get_product_by_name
from routes.order import add_order, get_orders, generate_whatapp_url, log_order, get_order_history, update_status
from routes.expiry import expiry_products

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://pharmacymanagement-five.vercel.app/", "http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Create_database()

@app.post("/register")
def register_user(register: UserSignUp):
    result = create_account(register)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.post("/login")
def loginin_user(userlogin: UserSignIn, response: Response):
    result = login_user(userlogin, response)
    if "error" in result: 
        raise HTTPException(status_code=400, detail= result["error"])
    return result

@app.get("/me")
def get_user_info(request: Request):
    result = get_user_info_from_request(request)
    if "error" in result:
        raise HTTPException(status_code=401, detail=result["error"])
    return result

@app.post("/refreshtoken")
def get_user_info_refresh(request: Request, response: Response):
    result = get_user_info_refresh_token(request, response)
    # if "error" in result:
    #     raise HTTPException(status_code=401, detail=result["error"])
    return result

@app.post("/logout")
def logout_user(response: Response):
    result = logout(response)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.post("/addproducts")
def create_product(create_product: list[AddProduct], token:str = Depends(get_token_from_cookies)):
    result = add_product(create_product, token)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.patch("/update/{product_id}")
def update_product(update: UpdateProduct,  product_id:int, token:str = Depends(get_token_from_cookies)):
    result = edit_product(update, product_id, token)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.delete("/delete/{product_id}")
def remove_product(product_id:int, token:str = Depends(get_token_from_cookies)):
    result = delete_product(product_id, token)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.get("/getproduct")
def show_product(token:str = Depends(get_token_from_cookies)):
    result = get_product(token)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.patch("/expiryproduct")
def expired_product(token: str=Depends(get_token_from_cookies)):
    result = expiry_products(token)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.get("/getproductbyname")
def show_product_by_name(name: str, token:str = Depends(get_token_from_cookies)):
    result = get_product_by_name(name, token)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.post("/addorder")
def auto_order(token: str=Depends(get_token_from_cookies)):
    result = add_order(token)
    if "error" in result:
        raise HTTPException(status_code=401, detail=result["error"])
    return result


@app.get("/getorder")
def send_order(token: str=Depends(get_token_from_cookies)):
    result = get_orders(token)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.get("/sendorder")
def send_order(token: str = Depends(get_token_from_cookies)):
    result = generate_whatapp_url(token)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return {"whatsapp_url": result}

@app.post("/orders")
def log_list_order(payload: Any = Body(default=None), token: str = Depends(get_token_from_cookies)):
    print(payload)
    if isinstance(payload, dict):
        items = payload.get("items", [])
        confirm_duplicate = payload.get("confirm_duplicate", False)
    else:
        items = payload if isinstance(payload, list) else []
        confirm_duplicate = False

    if not isinstance(items, list):
        raise HTTPException(status_code=400, detail="items must be a list")

    result = log_order(items, token, confirm_duplicate)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.get("/orderhistory")
def order_history(token: str = Depends(get_token_from_cookies)):
    result = get_order_history(token)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.patch("/update_status/{status}")
def update_product_status(status:str, token:str = Depends(get_token_from_cookies)):
    result = update_status(status, token)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result