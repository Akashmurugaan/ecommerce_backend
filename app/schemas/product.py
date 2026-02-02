from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int
class ProductStockUpdate(BaseModel):
    stock: int = Field(..., ge=0)
    
class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    description: str | None = None    

class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    description: str
    stock: int

    class Config:
        from_attributes = True
