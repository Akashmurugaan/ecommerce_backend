from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.models.user import User
from app.db.session import get_db
from app.db.models.category import Category
from app.schemas.category import CategoryCreate, CategoryOut
from app.dependencies.roles import require_roles

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
