# app/schemas/admin.py

# from pydantic import BaseModel
from pydantic import BaseModel, EmailStr

class AdminUserResponse(BaseModel):
    id: int
    email: str
    role: str



class SellerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str

class SellerResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    role: str

    class Config:
        from_attributes = True

