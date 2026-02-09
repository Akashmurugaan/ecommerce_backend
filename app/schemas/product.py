from pydantic import BaseModel, Field
from typing import List

# class ProductCreate(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     stock: int

class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    category_id: int
    size_ids: List[int]   # seller selects multiple sizes
    price: float
    stock: int


class ProductStockUpdate(BaseModel):
    stock: int = Field(..., ge=0)
    
class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    description: str | None = None    


class ProductOut(BaseModel):
    name: str
    description: str | None
    category: str
    size: list[str]
    price: float
    stock: int    

# class ProductOut(BaseModel):
#     id: int
#     name: str
#     price: float
#     description: str
#     stock: int

    class Config:
        from_attributes = True
