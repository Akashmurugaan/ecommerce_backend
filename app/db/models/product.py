# from sqlalchemy import Column, Integer, String, Float, ForeignKey
# from sqlalchemy.orm import relationship
# from app.db.base import Base

# class Product(Base):
#     __tablename__ = "products"

#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     description = Column(String)
#     price = Column(Float, nullable=False)
#     stock = Column(Integer, default=0)

#     seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)

#     seller = relationship("User", back_populates="products")


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
    seller_id = Column(Integer, ForeignKey("users.id"))

    seller = relationship(
        "User",
        back_populates="products"
    )
