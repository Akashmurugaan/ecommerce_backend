from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.roles import require_roles
from app.db.models.user import User
from app.schemas.order import OrderOut
from app.services.order_service import get_my_order_detail, get_my_orders


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/me", response_model=list[OrderOut])
def my_orders(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("USER")),
):
    return get_my_orders(db, user_id=user.id)


@router.get("/{order_id}", response_model=OrderOut)
def my_order_detail(
    order_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("USER")),
):
    return get_my_order_detail(db, user_id=user.id, order_id=order_id)

