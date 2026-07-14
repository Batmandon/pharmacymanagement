from pydantic import BaseModel, EmailStr, Field
from datetime import date

class UserSignUp(BaseModel):
    name: str = Field(min_length=3, max_length=20)
    pharmacy_name: str = Field(max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=20)

class UserSignIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class UserRefresh(BaseModel):
    token: str

class AddProduct(BaseModel):
    medicine_name: str = Field(max_length=20)
    batch_no: str = Field(max_length=15)
    quantity: int
    price: int
    expiry_date: date

class UpdateProduct(BaseModel):
    medicine_name: str = Field(max_length=20)
    batch_no: str = Field(max_length=15)
    quantity: int
    expiry_date: date 
    price: int

class Order(BaseModel):
    id: int
    quantity: int

class OrderLogRequest(BaseModel):
    items: list
    confirm_duplicate: bool = False