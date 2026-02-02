# from sqlalchemy import Column, Integer, String, Boolean
# from app.db.base import Base

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     email = Column(String, unique=True, index=True)
#     phone = Column(String, unique=True)
#     password_hash = Column(String)
#     role = Column(String, default="USER")
#     is_active = Column(Boolean, default=True)


from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True)
    password_hash = Column(String)
    role = Column(String, default="USER")
    is_active = Column(Boolean, default=True)

    # # ✅ THIS WAS MISSING
    products = relationship(
        "Product",
        back_populates="seller",
        cascade="all, delete"
    )
