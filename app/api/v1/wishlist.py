from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
# from app.core.security import get_current_user
from app.dependencies.roles import require_roles
from app.db.models.user import User
from app.services.wishlist_service import (
    add_to_wishlist,
    get_wishlist,
    remove_from_wishlist
)

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])


@router.post("/{product_id}")
def add_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("USER"))
):
    return add_to_wishlist(db, current_user.id, product_id)


@router.get("/")
def view_wishlist(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("USER"))
):
    return get_wishlist(db, current_user.id)


@router.delete("/{item_id}")
def remove_product(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("USER"))
):
    return remove_from_wishlist(db, current_user.id, item_id)
