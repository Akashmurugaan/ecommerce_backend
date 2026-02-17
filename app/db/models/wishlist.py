# from sqlalchemy import Column, Integer, ForeignKey
# from app.db.base import Base

# class Wishlist(Base):
#     __tablename__ = "wishlists"

#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     product_id = Column(Integer, ForeignKey("products.id"), nullable=False)


from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Wishlist(Base):
    __tablename__ = "wishlists"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    items = relationship(
        "WishlistItem",
        back_populates="wishlist",
        cascade="all, delete-orphan"
    )
