# app/db/models/product.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)

    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    seller = relationship("User", back_populates="products")
    category = relationship("Category")
    sizes = relationship(
        "ProductMeasurement",
        back_populates="product",
        cascade="all, delete"   
    )



# from sqlalchemy import Column, Integer, String, Float, ForeignKey
# from sqlalchemy.orm import relationship
# from app.db.base import Base

# class Product(Base):
#     __tablename__ = "products"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     description = Column(String)
#     price = Column(Float, nullable=False)
#     stock = Column(Integer, default=0)
#     seller_id = Column(Integer, ForeignKey("users.id"))

#     seller = relationship(
#         "User",
#         back_populates="products"
#     )
