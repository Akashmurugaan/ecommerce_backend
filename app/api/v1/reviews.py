from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.db.models.user import User
from app.schemas.review import ReviewCreate, ReviewOut
from app.services.review_service import list_product_reviews, upsert_product_review


router = APIRouter(prefix="/products", tags=["Reviews"])


@router.get("/{product_id}/reviews", response_model=list[ReviewOut])
def get_reviews(
    product_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return list_product_reviews(db, product_id=product_id, skip=skip, limit=limit)


@router.post("/{product_id}/reviews", response_model=ReviewOut)
def add_review(
    product_id: int,
    data: ReviewCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return upsert_product_review(
        db,
        product_id=product_id,
        user_id=user.id,
        rating=data.rating,
        comment=data.comment,
    )

