from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.models.user import User
from app.db.session import get_db
from app.db.models.category import Category
from app.schemas.category import CategoryCreate, CategoryOut
from app.schemas.product import ProductOut
from app.dependencies.roles import require_roles
from app.services.product_service import get_products_by_category

router = APIRouter(prefix="/categories", tags=["Categories"])
@router.post("/", response_model=CategoryOut)
def create_category(
    data: CategoryCreate,

    db: Session = Depends(get_db),
    user : User=Depends(require_roles("ADMIN"))
):
    if db.query(Category).filter(Category.name == data.name).first():
        raise HTTPException(400, "Category already exists")

    category = Category(name=data.name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.get("/", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.get("/{category_id}/products", response_model=list[ProductOut])
def list_products_by_category(
    category_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    return get_products_by_category(db, category_id=category_id, skip=skip, limit=limit)
