from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base


class WishlistItem(Base):
    __tablename__ = "wishlist_items"

    id = Column(Integer, primary_key=True)
    wishlist_id = Column(Integer, ForeignKey("wishlists.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    wishlist = relationship("Wishlist", back_populates="items")
    product = relationship("Product")

    __table_args__ = (
        UniqueConstraint("wishlist_id", "product_id"),
    )
