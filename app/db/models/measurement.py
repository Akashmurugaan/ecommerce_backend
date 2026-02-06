# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from app.db.base import Base

# class Measurement(Base):
#     __tablename__ = "measurements"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, unique=True, nullable=False)
#     seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)

#     seller = relationship("User", back_populates="measurements")

from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base

class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    seller = relationship("User")
    category = relationship("Category")

    __table_args__ = (
        UniqueConstraint("name", "seller_id", "category_id"),
    )
