from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.models.wishlist import Wishlist
from app.db.models.wishlist_item import WishlistItem
from app.db.models.product import Product


def get_or_create_wishlist(db: Session, user_id: int):
    wishlist = db.query(Wishlist).filter(Wishlist.user_id == user_id).first()

    if not wishlist:
        wishlist = Wishlist(user_id=user_id)
        db.add(wishlist)
        db.commit()
        db.refresh(wishlist)

    return wishlist


def add_to_wishlist(db: Session, user_id: int, product_id: int):

    wishlist = get_or_create_wishlist(db, user_id)

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")

    existing = db.query(WishlistItem).filter(
        WishlistItem.wishlist_id == wishlist.id,
        WishlistItem.product_id == product_id
    ).first()

    if existing:
        return {"message": "Product already in wishlist"}

    item = WishlistItem(
        wishlist_id=wishlist.id,
        product_id=product_id
    )

    db.add(item)
    db.commit()

    return {"message": "Added to wishlist"}


def get_wishlist(db: Session, user_id: int):

    wishlist = get_or_create_wishlist(db, user_id)

    result = []

    for item in wishlist.items:
        result.append({
            "item_id": item.id,
            "product": item.product,
        })

    return {"items": result}


def remove_from_wishlist(db: Session, user_id: int, item_id: int):

    wishlist = get_or_create_wishlist(db, user_id)

    item = db.query(WishlistItem).filter(
        WishlistItem.id == item_id,
        WishlistItem.wishlist_id == wishlist.id
    ).first()

    if not item:
        raise HTTPException(404, "Wishlist item not found")

    db.delete(item)
    db.commit()

    return {"message": "Removed from wishlist"}
