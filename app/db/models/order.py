from sqlalchemy import Column, Integer, ForeignKey, String, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, nullable=False, default="PENDING")

    total_amount = Column(Float, nullable=False, default=0.0)
    payment_method = Column(String, nullable=False, default="COD")

    shipping_full_name = Column(String, nullable=False)
    shipping_phone = Column(String, nullable=False)
    shipping_line1 = Column(String, nullable=False)
    shipping_line2 = Column(String, nullable=True)
    shipping_city = Column(String, nullable=False)
    shipping_state = Column(String, nullable=True)
    shipping_postal_code = Column(String, nullable=False)
    shipping_country = Column(String, nullable=False, default="India")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
    )
