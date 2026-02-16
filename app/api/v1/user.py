from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.product import ProductOut
from app.services.product_service import (
    get_all_products,
    get_new_arrivals,
    get_products_by_category,
)

router = APIRouter(prefix="/user", tags=["User"])


# Public endpoints for users (no login required)
@router.get("/products", response_model=list[ProductOut])
def user_all_products(db: Session = Depends(get_db)):
    return get_all_products(db)


@router.get("/products/new-arrivals", response_model=list[ProductOut])
def user_new_arrivals(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return get_new_arrivals(db, limit=limit)


@router.get("/categories/{category_id}/products", response_model=list[ProductOut])
def user_products_by_category(
    category_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    return get_products_by_category(db, category_id=category_id, skip=skip, limit=limit)
