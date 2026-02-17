from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.models.cart import Cart
from app.db.models.cart_item import CartItem
from app.db.models.product import Product
from app.schemas.cart import AddToCart


def get_or_create_cart(db: Session, user_id: int):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    return cart


def add_to_cart(db: Session, user_id: int, data: AddToCart):

    product = db.query(Product).filter(Product.id == data.product_id).first()

    if not product:
        raise HTTPException(404, "Product not found")

    if data.quantity <= 0:
        raise HTTPException(400, "Quantity must be greater than 0")

    cart = get_or_create_cart(db, user_id)

    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == data.product_id,
        CartItem.size_id == data.size_id
    ).first()

    if existing_item:
        existing_item.quantity += data.quantity
    else:
        db.add(
            CartItem(
                cart_id=cart.id,
                product_id=data.product_id,
                size_id=data.size_id,
                quantity=data.quantity
            )
        )

    db.commit()
    return {"message": "Added to cart"}



def get_cart(db: Session, user_id: int):

    cart = get_or_create_cart(db, user_id)

    result = []
    total = 0

    for item in cart.items:
        subtotal = item.product.price * item.quantity
        total += subtotal

        result.append({
            "item_id": item.id,
            "product_id": item.product.id,
            "product_name": item.product.name,
            "size_id": item.size.id,
            "size": item.size.name,
            "price": item.product.price,
            "quantity": item.quantity,
            "subtotal": subtotal
        })

    return {
        "cart_id": cart.id,
        "items": result,
        "total_amount": total
    }


def remove_cart_item(db: Session, user_id: int, item_id: int):

    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        raise HTTPException(404, "Cart not found")

    item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()

    if not item:
        raise HTTPException(404, "Item not found")

    db.delete(item)
    db.commit()

    return {"message": "Item removed"}



def update_cart_item_quantity(db: Session, user_id: int, item_id: int, quantity: int):

    cart = get_or_create_cart(db, user_id)

    item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()

    if not item:
        raise HTTPException(404, "Cart item not found")

    if quantity <= 0:
        db.delete(item)
        db.commit()
        return {"message": "Item removed from cart"}

    if quantity > item.product.stock:
        raise HTTPException(400, "Not enough stock")

    item.quantity = quantity
    db.commit()

    return {"message": "Quantity updated"}
