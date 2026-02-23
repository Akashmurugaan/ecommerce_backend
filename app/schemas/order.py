from pydantic import BaseModel, Field

from app.schemas.address import AddressCreate


class OrderItemOut(BaseModel):
    id: int
    product_id: int
    seller_id: int
    size_id: int
    product_name: str
    size_name: str
    quantity: int
    unit_price: float
    subtotal: float

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: int
    status: str
    total_amount: float
    payment_method: str

    shipping_full_name: str | None = None
    shipping_phone: str | None = None
    shipping_line1: str | None = None
    shipping_line2: str | None = None
    shipping_city: str | None = None
    shipping_state: str | None = None
    shipping_postal_code: str | None = None
    shipping_country: str | None = None

    items: list[OrderItemOut]

    class Config:
        from_attributes = True


class CheckoutCartRequest(BaseModel):
    address_id: int | None = None
    new_address: AddressCreate | None = None
    save_new_address: bool = True
    payment_method: str = "COD"


class CheckoutBuyNowRequest(BaseModel):
    product_id: int
    size_id: int
    quantity: int = Field(..., ge=1)

    address_id: int | None = None
    new_address: AddressCreate | None = None
    save_new_address: bool = True
    payment_method: str = "COD"


class SellerOrderItemOut(BaseModel):
    order_id: int
    order_status: str

    buyer_id: int
    buyer_name: str

    shipping_full_name: str | None
    shipping_phone: str | None
    shipping_line1: str | None
    shipping_line2: str | None
    shipping_city: str | None
    shipping_state: str | None
    shipping_postal_code: str | None
    shipping_country: str | None

    product_id: int
    product_name: str
    size_id: int
    size_name: str
    quantity: int
    unit_price: float
    subtotal: float

