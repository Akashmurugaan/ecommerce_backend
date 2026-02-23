from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.roles import require_roles
from app.db.models.user import User
from app.schemas.order import CheckoutBuyNowRequest, CheckoutCartRequest, OrderOut
from app.services.order_service import buy_now, checkout_cart


router = APIRouter(prefix="/checkout", tags=["Checkout"])


@router.post("/cart", response_model=OrderOut)
def checkout_from_cart(
    data: CheckoutCartRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("USER")),
):
    return checkout_cart(db, user_id=user.id, data=data)


@router.post("/buy-now", response_model=OrderOut)
def checkout_buy_now(
    data: CheckoutBuyNowRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("USER")),
):
    return buy_now(db, user_id=user.id, data=data)

