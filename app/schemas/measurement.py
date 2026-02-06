# from pydantic import BaseModel

# class MeasurementCreate(BaseModel):
#     name: str

# class MeasurementOut(BaseModel):
#     id: int
#     name: str

#     class Config:
#         from_attributes = True


from pydantic import BaseModel
from typing import List

class MeasurementCreate(BaseModel):
    category_id: int
    name: str

class MeasurementOut(BaseModel):
    id: int
    name: str
    category_id: int

    class Config:
        from_attributes = True
