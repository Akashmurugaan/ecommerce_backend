# app/db/models/product_measurement.py
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base

class ProductMeasurement(Base):
    __tablename__ = "product_measurements"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    measurement_id = Column(Integer, ForeignKey("measurements.id", ondelete="CASCADE"), nullable=False)

    product = relationship("Product", back_populates="sizes")
    measurement = relationship("Measurement", back_populates="products")
