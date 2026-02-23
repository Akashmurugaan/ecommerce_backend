from fastapi import HTTPException
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import Session, joinedload

from app.db.models.address import Address
from app.db.models.cart import Cart
from app.db.models.cart_item import CartItem
from app.db.models.measurement import Measurement
from app.db.models.order import Order
from app.db.models.order_item import OrderItem
from app.db.models.product import Product
from app.db.models.product_measurement import ProductMeasurement
from app.db.models.user import User
from app.schemas.address import AddressCreate
from app.schemas.order import CheckoutBuyNowRequest, CheckoutCartRequest
from app.services.address_service import create_address


def _resolve_shipping_address(
    db: Session,
    *,
    user_id: int,
    address_id: int | None,
    new_address: AddressCreate | None,
    save_new_address: bool,
):
    if address_id is not None and address_id <= 0:
        address_id = None

    if address_id is not None:
        try:
            address = (
                db.query(Address)
                .filter(Address.id == address_id, Address.user_id == user_id)
                .first()
            )
        except ProgrammingError as exc:
            msg = str(getattr(exc, "orig", exc))
            if "relation" in msg and "addresses" in msg and "does not exist" in msg:
                raise HTTPException(500, "Database not migrated. Run: alembic upgrade head")
            raise
        if not address:
            raise HTTPException(404, "Address not found")
        return address

    if new_address is not None:
        if save_new_address:
            return create_address(db, user_id=user_id, data=new_address, commit=False)
        return new_address

    try:
        address = (
            db.query(Address)
            .filter(Address.user_id == user_id, Address.is_default.is_(True))
            .first()
        )
    except ProgrammingError as exc:
        msg = str(getattr(exc, "orig", exc))
        if "relation" in msg and "addresses" in msg and "does not exist" in msg:
            raise HTTPException(500, "Database not migrated. Run: alembic upgrade head")
        raise
    if not address:
        raise HTTPException(400, "No address found. Add an address or select an existing one.")
    return address


def _apply_shipping_fields(order: Order, address):
    order.shipping_full_name = getattr(address, "full_name")
    order.shipping_phone = getattr(address, "phone")
    order.shipping_line1 = getattr(address, "line1")
    order.shipping_line2 = getattr(address, "line2")
    order.shipping_city = getattr(address, "city")
    order.shipping_state = getattr(address, "state")
    order.shipping_postal_code = getattr(address, "postal_code")
    order.shipping_country = getattr(address, "country")


def _validate_product_size(db: Session, *, product_id: int, size_id: int):
    ok = (
        db.query(ProductMeasurement.id)
        .filter(
            ProductMeasurement.product_id == product_id,
            ProductMeasurement.measurement_id == size_id,
        )
        .first()
    )
    if not ok:
        raise HTTPException(400, "Invalid size for product")


def checkout_cart(db: Session, *, user_id: int, data: CheckoutCartRequest):
    cart = (
        db.query(Cart)
        .options(
            joinedload(Cart.items).joinedload(CartItem.product),
            joinedload(Cart.items).joinedload(CartItem.size),
        )
        .filter(Cart.user_id == user_id)
        .first()
    )
    if not cart or not cart.items:
        raise HTTPException(400, "Cart is empty")

    shipping = _resolve_shipping_address(
        db,
        user_id=user_id,
        address_id=data.address_id,
        new_address=data.new_address,
        save_new_address=data.save_new_address,
    )

    # Validate sizes & calculate per-product required quantities
    required_qty: dict[int, int] = {}
    for item in cart.items:
        _validate_product_size(db, product_id=item.product_id, size_id=item.size_id)
        required_qty[item.product_id] = required_qty.get(item.product_id, 0) + item.quantity

    # Lock products in stable order to avoid deadlocks
    product_ids = sorted(required_qty.keys())
    products = (
        db.query(Product)
        .filter(Product.id.in_(product_ids))
        .with_for_update()
        .all()
    )
    products_by_id = {p.id: p for p in products}
    missing = [pid for pid in product_ids if pid not in products_by_id]
    if missing:
        raise HTTPException(404, f"Products not found: {missing}")

    for pid, qty in required_qty.items():
        if qty <= 0:
            raise HTTPException(400, "Invalid quantity in cart")
        if products_by_id[pid].stock < qty:
            raise HTTPException(400, f"Not enough stock for product_id={pid}")

    order = Order(
        user_id=user_id,
        status="PENDING",
        payment_method=data.payment_method,
    )
    _apply_shipping_fields(order, shipping)

    total = 0.0
    db.add(order)
    db.flush()

    for item in cart.items:
        product = products_by_id[item.product_id]
        unit_price = float(product.price)
        subtotal = unit_price * item.quantity
        total += subtotal

        db.add(
            OrderItem(
                order_id=order.id,
                product_id=product.id,
                seller_id=product.seller_id,
                size_id=item.size_id,
                product_name=product.name,
                size_name=item.size.name if item.size else str(item.size_id),
                quantity=item.quantity,
                unit_price=unit_price,
                subtotal=subtotal,
            )
        )

    for pid, qty in required_qty.items():
        products_by_id[pid].stock -= qty

    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete(synchronize_session=False)

    order.total_amount = total
    db.commit()
    db.refresh(order)
    return order


def buy_now(db: Session, *, user_id: int, data: CheckoutBuyNowRequest):
    product = db.query(Product).filter(Product.id == data.product_id).with_for_update().first()
    if not product:
        raise HTTPException(404, "Product not found")

    if data.quantity <= 0:
        raise HTTPException(400, "Quantity must be greater than 0")

    _validate_product_size(db, product_id=product.id, size_id=data.size_id)

    if product.stock < data.quantity:
        raise HTTPException(400, "Not enough stock")

    size = db.query(Measurement).filter(Measurement.id == data.size_id).first()
    if not size:
        raise HTTPException(404, "Size not found")

    shipping = _resolve_shipping_address(
        db,
        user_id=user_id,
        address_id=data.address_id,
        new_address=data.new_address,
        save_new_address=data.save_new_address,
    )

    order = Order(
        user_id=user_id,
        status="PENDING",
        payment_method=data.payment_method,
    )
    _apply_shipping_fields(order, shipping)

    unit_price = float(product.price)
    subtotal = unit_price * data.quantity
    order.total_amount = subtotal

    db.add(order)
    db.flush()

    db.add(
        OrderItem(
            order_id=order.id,
            product_id=product.id,
            seller_id=product.seller_id,
            size_id=data.size_id,
            product_name=product.name,
            size_name=size.name,
            quantity=data.quantity,
            unit_price=unit_price,
            subtotal=subtotal,
        )
    )

    product.stock -= data.quantity

    db.commit()
    db.refresh(order)
    return order


def get_my_orders(db: Session, *, user_id: int):
    return (
        db.query(Order)
        .options(joinedload(Order.items))
        .filter(Order.user_id == user_id)
        .order_by(Order.id.desc())
        .all()
    )


def get_my_order_detail(db: Session, *, user_id: int, order_id: int):
    order = (
        db.query(Order)
        .options(joinedload(Order.items))
        .filter(Order.id == order_id, Order.user_id == user_id)
        .first()
    )
    if not order:
        raise HTTPException(404, "Order not found")
    return order


def seller_order_items(db: Session, *, seller_id: int):
    rows = (
        db.query(OrderItem, Order, User)
        .join(Order, Order.id == OrderItem.order_id)
        .join(User, User.id == Order.user_id)
        .filter(OrderItem.seller_id == seller_id)
        .order_by(Order.id.desc(), OrderItem.id.desc())
        .all()
    )

    result: list[dict] = []
    for oi, order, buyer in rows:
        result.append(
            {
                "order_id": order.id,
                "order_status": order.status,
                "buyer_id": buyer.id,
                "buyer_name": buyer.name,
                "shipping_full_name": order.shipping_full_name,
                "shipping_phone": order.shipping_phone,
                "shipping_line1": order.shipping_line1,
                "shipping_line2": order.shipping_line2,
                "shipping_city": order.shipping_city,
                "shipping_state": order.shipping_state,
                "shipping_postal_code": order.shipping_postal_code,
                "shipping_country": order.shipping_country,
                "product_id": oi.product_id,
                "product_name": oi.product_name,
                "size_id": oi.size_id,
                "size_name": oi.size_name,
                "quantity": oi.quantity,
                "unit_price": oi.unit_price,
                "subtotal": oi.subtotal,
            }
        )
    return result
