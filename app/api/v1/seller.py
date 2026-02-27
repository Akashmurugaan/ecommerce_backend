from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.roles import require_roles
from app.db.models.user import User
from app.schemas.order import (
    OrderStatusUpdateOut,
    OrderStatusUpdateRequest,
    SellerOrderItemOut,
)
from app.services.order_service import seller_order_items, seller_update_order_status


router = APIRouter(prefix="/seller", tags=["Seller"])


@router.get("/orders", response_model=list[SellerOrderItemOut])
def my_seller_orders(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("SELLER", "ADMIN")),
):
    return seller_order_items(db, seller_id=user.id)


@router.patch("/orders/{order_id}/status", response_model=OrderStatusUpdateOut)
def update_order_status(
    order_id: int,
    data: OrderStatusUpdateRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("SELLER", "ADMIN")),
):
    return seller_update_order_status(
        db,
        seller_id=user.id,
        order_id=order_id,
        new_status=data.status,
        is_admin=user.role == "ADMIN",
    )
