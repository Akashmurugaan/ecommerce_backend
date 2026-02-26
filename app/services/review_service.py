from fastapi import HTTPException
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import exists
from sqlalchemy.orm import Session, joinedload

from app.db.models.order import Order
from app.db.models.order_item import OrderItem
from app.db.models.product import Product
from app.db.models.review import Review


def _serialize_review(review: Review):
    return {
        "id": review.id,
        "product_id": review.product_id,
        "user_id": review.user_id,
        "user_name": review.user.name if review.user else "",
        "rating": review.rating,
        "comment": review.comment,
        "created_at": review.created_at,
    }


def list_product_reviews(
    db: Session,
    *,
    product_id: int,
    skip: int = 0,
    limit: int = 20,
):
    product_exists = db.query(Product.id).filter(Product.id == product_id).first()
    if not product_exists:
        raise HTTPException(404, "Product not found")

    try:
        rows = (
            db.query(Review)
            .options(joinedload(Review.user))
            .filter(Review.product_id == product_id)
            .order_by(Review.id.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    except ProgrammingError as exc:
        msg = str(getattr(exc, "orig", exc))
        if "relation" in msg and "reviews" in msg and "does not exist" in msg:
            raise HTTPException(500, "Database not migrated. Run: alembic upgrade head")
        raise
    return [_serialize_review(r) for r in rows]


def upsert_product_review(
    db: Session,
    *,
    product_id: int,
    user_id: int,
    rating: int,
    comment: str | None,
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")

    try:
        has_bought = db.query(
            exists().where(
                (Order.user_id == user_id)
                & (OrderItem.order_id == Order.id)
                & (OrderItem.product_id == product_id)
            )
        ).scalar()
    except ProgrammingError as exc:
        msg = str(getattr(exc, "orig", exc))
        if "relation" in msg and "reviews" in msg and "does not exist" in msg:
            raise HTTPException(500, "Database not migrated. Run: alembic upgrade head")
        raise
    if not has_bought:
        raise HTTPException(403, "You can review only products you have purchased")

    try:
        existing = (
            db.query(Review)
            .filter(Review.product_id == product_id, Review.user_id == user_id)
            .first()
        )
    except ProgrammingError as exc:
        msg = str(getattr(exc, "orig", exc))
        if "relation" in msg and "reviews" in msg and "does not exist" in msg:
            raise HTTPException(500, "Database not migrated. Run: alembic upgrade head")
        raise
    if existing:
        existing.rating = rating
        existing.comment = comment
        db.commit()
        db.refresh(existing)
        return _serialize_review(existing)

    review = Review(
        product_id=product_id,
        user_id=user_id,
        rating=rating,
        comment=comment,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return _serialize_review(review)
