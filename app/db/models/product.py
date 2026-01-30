from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    seller_id = Column(Integer, ForeignKey("users.id"))
