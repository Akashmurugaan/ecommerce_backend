# app/api/admin.py

from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.dependencies.admin import admin_required
from app.services import admin_service
from app.schemas.admin import SellerCreate, SellerResponse
from app.services.admin_service import (
    create_seller,
    get_all_sellers,
    delete_seller,
    update_user_status
)
from app.db.models.user import User

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(admin_required)]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#seller
@router.post("/seller", response_model=SellerResponse)
def add_seller(
    data: SellerCreate,
    admin: User = Depends(admin_required),
    db: Session = Depends(get_db)
):
    return create_seller(db, data)

@router.get("/sellers", response_model=list[SellerResponse])
def view_sellers(
    admin: User = Depends(admin_required),
    db: Session = Depends(get_db)
):
    return get_all_sellers(db)

@router.delete("/seller/{seller_id}")
def remove_seller(
    seller_id: int,
    admin: User = Depends(admin_required),
    db: Session = Depends(get_db)
):
    success = delete_seller(db, seller_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seller not found"
        )

    return {"message": "Seller deleted successfully"}

# 👤 USERS
@router.get("/users")
def list_users(db: Session = Depends(get_db)):
    return admin_service.get_all_users(db)

# @router.put("/users/{user_id}/block")
# def block_user(user_id: int, db: Session = Depends(get_db)):
#     user = admin_service.block_user(db, user_id)
#     if not user:
#         raise HTTPException(404, "User not found")
#     return {"message": "User blocked"}

@router.put("/users/{user_id}/block")

def block_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin = Depends(admin_required)
):
    return update_user_status(db, user_id, is_active=False)


@router.put("/users/{user_id}/unblock")
def unblock_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin = Depends(admin_required)
):
    return update_user_status(db, user_id, is_active=True)

# 📦 PRODUCTS
@router.get("/products")
def list_all_products(db: Session = Depends(get_db)):
    return admin_service.get_all_products(db)

@router.delete("/products/{product_id}")
def admin_delete_product(product_id: int, db: Session = Depends(get_db)):
    result = admin_service.delete_product(db, product_id)
    if not result:
        raise HTTPException(404, "Product not found")
    return {"message": "Product deleted"}
