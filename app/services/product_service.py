from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.schemas.product import ProductCreate, ProductUpdate
from app.db.models.product import Product
from app.db.models.user import User


def create_product(db: Session, data: ProductCreate, seller_id: int):
    product = Product(
        name=data.name,
        description=data.description,
        price=data.price,
        stock=data.stock,
        seller_id=seller_id,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
def get_products_by_seller(db: Session, seller_id: int):
    return (
        db.query(Product)
        .filter(Product.seller_id == seller_id)
        .all()
    )

def update_product(
    db: Session,
    product_id: int,
    data: ProductUpdate,
    user: User
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(404, "Product not found")

    # 🔐 Authorization check
    if user.role == "SELLER" and product.seller_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can update only your own products"
        )

    for key, value in data.dict(exclude_unset=True).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product

def update_product_stock(
    db: Session,
    product_id: int,
    seller_id: int,
    stock: int
):
    product = (
        db.query(Product)
        .filter(
            Product.id == product_id,
            Product.seller_id == seller_id   # 🔐 ownership check
        )
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found or not owned by seller"
        )

    product.stock = stock
    db.commit()
    db.refresh(product)

    return product


def delete_product(db: Session, product_id: int, user: User):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(404, "Product not found")

    # 🔐 Authorization check
    if user.role == "SELLER" and product.seller_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can delete only your own products"
        )

    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

def get_all_products(db: Session):
    return db.query(Product).all()


def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


