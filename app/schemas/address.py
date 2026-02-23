from pydantic import BaseModel, Field


class AddressCreate(BaseModel):
    full_name: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=5)
    line1: str = Field(..., min_length=1)
    line2: str | None = None
    city: str = Field(..., min_length=1)
    state: str | None = None
    postal_code: str = Field(..., min_length=1)
    country: str = Field(default="India", min_length=1)
    is_default: bool = False


class AddressUpdate(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    line1: str | None = None
    line2: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    country: str | None = None


class AddressOut(BaseModel):
    id: int
    full_name: str
    phone: str
    line1: str
    line2: str | None
    city: str
    state: str | None
    postal_code: str
    country: str
    is_default: bool

    class Config:
        from_attributes = True

