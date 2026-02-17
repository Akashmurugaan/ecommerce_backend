from pydantic import BaseModel
from typing import List

class AddToCart(BaseModel):
    product_id: int
    size_id: int
    quantity: int


class CartItemOut(BaseModel):
    item_id: int
    product_id: int
    product_name: str
    size_id: int
    size: str
    price: float
    quantity: int
    subtotal: float


class UpdateCartQuantity(BaseModel):
    item_id: int
    quantity: int

class CartOut(BaseModel):
    items: List[CartItemOut]
    total_amount: float
