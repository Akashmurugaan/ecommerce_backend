from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.schemas.product import ProductCreate, ProductUpdate
from app.db.models.product import Product
from app.db.models.product_measurement import ProductMeasurement
from app.db.models.measurement import Measurement
from app.db.models.user import User


# def create_product(db: Session, data: ProductCreate, seller_id: int):
#     product = Product(
#         name=data.name,
#         description=data.description,
#         category_id= data.category_id,
#         size_ids= data.size_ids,     
#         price=data.price,
#         stock=data.stock,
#         seller_id=seller_id,
#     )
#     db.add(product)
#     db.commit()
#     db.refresh(product)
#     return product


def create_product(db: Session, data: ProductCreate, seller_id: int):
    product = Product(
        name=data.name,
        description=data.description,
        category_id=data.category_id,
        price=data.price,
        stock=data.stock,
        seller_id=seller_id,
    )
    db.add(product)
    db.flush()  # 👈 VERY IMPORTANT (get product.id before commit)

    # ✅ attach sizes
    for size_id in data.size_ids:
        measurement = db.query(Measurement).filter(
            Measurement.id == size_id,
            Measurement.seller_id == seller_id
        ).first()

        if not measurement:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid measurement ID: {size_id}"
            )

        db.add(
            ProductMeasurement(
                product_id=product.id,
                measurement_id=size_id
            )
        )

    db.commit()
    db.refresh(product)
    return product




#  def get_products_by_seller(db: Session, seller_id: int):
#     return (
#         db.query(Product)
#         .filter(Product.seller_id == seller_id)
#         .all()
#     )

def get_all_products(db: Session):
    products = db.query(Product).all()

    result = []

    for product in products:
        sizes = [
            pm.measurement.name
            for pm in product.sizes
        ]

        result.append({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "category": product.category.name,
            "size": [                             
                pm.measurement.name
                for pm in product.sizes
            ],
            "price": product.price,
            "stock": product.stock,
        })

    return result


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

# def get_all_products(db: Session):
#     return db.query(Product).all()


def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


