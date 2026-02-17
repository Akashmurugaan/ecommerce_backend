from pydantic import BaseModel
from app.schemas.product import ProductOut


class WishlistItemOut(BaseModel):
    item_id: int
    product: ProductOut

    class Config:
        from_attributes = True


class WishlistOut(BaseModel):
    items: list[WishlistItemOut]
