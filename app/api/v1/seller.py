from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.roles import require_roles
from app.db.models.user import User
from app.schemas.order import SellerOrderItemOut
from app.services.order_service import seller_order_items


router = APIRouter(prefix="/seller", tags=["Seller"])


@router.get("/orders", response_model=list[SellerOrderItemOut])
def my_seller_orders(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("SELLER", "ADMIN")),
):
    return seller_order_items(db, seller_id=user.id)
