# app/db/models/admin.py

from sqlalchemy import Column, Integer, String
from app.db.base import Base
from pydantic import BaseModel

class UserStatusUpdate(BaseModel):
    is_active: bool


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, nullable=False)
    full_name = Column(String, nullable=True)
