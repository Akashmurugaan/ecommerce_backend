# app/services/admin_service.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models.user import User
from app.db.models.product import Product
from app.core.security import hash_password


def create_seller(db: Session, data):
    seller = User(
        name=data.name,
        email=data.email,
        phone=data.phone,
        password_hash=hash_password(data.password),
        role="SELLER"
    )
    db.add(seller)
    db.commit()
    db.refresh(seller)
    return seller


def get_all_sellers(db: Session):
    return db.query(User).filter(User.role == "SELLER").all()


def delete_seller(db: Session, seller_id: int):
    seller = db.query(User).filter(
        User.id == seller_id,
        User.role == "SELLER"
    ).first()

    if not seller:
        return False

    db.delete(seller)
    db.commit()
    return True

# 👤 USERS
def get_all_users(db: Session):
    return db.query(User).all()

# def block_user(db: Session, user_id: int):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         return None
#     user.is_active = False
#     db.commit()
#     return user


def update_user_status(
    db: Session,
    user_id: int,
    is_active: bool
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(404, "User not found")

    if user.role == "ADMIN":
        raise HTTPException(403, "Admin cannot be blocked")

    user.is_active = is_active
    db.commit()
    db.refresh(user)

    return user

# 📦 PRODUCTS
def get_all_products(db: Session):
    return db.query(Product).all()

def delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None
    db.delete(product)
    db.commit()
    return True
