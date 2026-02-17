from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.cart import AddToCart, CartOut, UpdateCartQuantity
from app.services.cart_service import (
    add_to_cart,
    get_cart,
    remove_cart_item,
    update_cart_item_quantity
)
# from app.core.security import require_roles
from app.dependencies.roles import require_roles
from app.db.models.user import User

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("/")
def add_item(
    data: AddToCart,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("USER"))
):
    return add_to_cart(db, user.id, data)


@router.get("/", response_model=CartOut)
def view_cart(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("USER"))
):
    return get_cart(db, user.id)


@router.put("/update-quantity")
def update_quantity(
    data: UpdateCartQuantity,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("USER"))
):
    return update_cart_item_quantity(
        db=db,
        user_id=current_user.id,
        item_id=data.item_id,
        quantity=data.quantity
    )


@router.delete("/{item_id}")
def remove_item(
    item_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("USER"))
):
    return remove_cart_item(db, user.id, item_id)
