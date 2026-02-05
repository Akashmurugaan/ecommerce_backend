from pydantic import BaseModel

class MeasurementCreate(BaseModel):
    name: str

class MeasurementOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
