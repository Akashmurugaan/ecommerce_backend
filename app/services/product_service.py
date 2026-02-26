from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.models.product import Product
from app.db.models.category import Category
from app.db.models.measurement import Measurement
from app.db.models.product_measurement import ProductMeasurement
from app.db.models.user import User
from app.schemas.product import ProductCreate, ProductUpdate

# 🔁 serializer (IMPORTANT)
def serialize_product(product: Product):
    size_names: list[str] = []
    size_ids: list[int] = []
    size_map: dict[str, int] = {}

    for pm in product.sizes:
        measurement = pm.measurement
        if not measurement:
            continue
        size_names.append(measurement.name)
        size_ids.append(measurement.id)
        size_map[measurement.name] = measurement.id

    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "category": product.category.name,
        "size": size_names,
        "size_ids": size_ids,
        "size_map": size_map,
        "price": product.price,
        "stock": product.stock,
        "image_url": f"/api/v1/products/{product.id}/image" if product.image_base64 else None,
    }


def set_product_image(
    db: Session,
    product_id: int,
    user: User,
    *,
    image_base64: str,
    image_mime: str | None = None,
    image_filename: str | None = None,
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")

    if user.role == "SELLER" and product.seller_id != user.id:
        raise HTTPException(403, "Not allowed")

    product.image_base64 = image_base64
    product.image_mime = image_mime
    product.image_filename = image_filename

    db.commit()
    db.refresh(product)
    return serialize_product(product)


def updated_product_image(
    db: Session,
    product_id: int,
    user: User,
    *,
    image_base64: str,
    image_mime: str | None = None,
    image_filename: str | None = None,
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")

    if user.role == "SELLER" and product.seller_id != user.id:
        raise HTTPException(403, "Not allowed")

    product.image_base64 = image_base64
    product.image_mime = image_mime
    product.image_filename = image_filename

    db.commit()
    db.refresh(product)
    return serialize_product(product)


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
    db.flush()

    for size_id in data.size_ids:
        measurement = db.query(Measurement).filter(
            Measurement.id == size_id,
            Measurement.seller_id == seller_id
        ).first()

        if not measurement:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid measurement ID {size_id}"
            )

        db.add(
            ProductMeasurement(
                product_id=product.id,
                measurement_id=size_id
            )
        )

    db.commit()
    db.refresh(product)
    return serialize_product(product)


def get_all_products(db: Session):
    products = db.query(Product).all()
    return [serialize_product(p) for p in products]

def get_new_arrivals(db: Session, *, limit: int = 10):
    products = (
        db.query(Product)
        .order_by(Product.id.desc())
        .limit(limit)
        .all()
    )
    return [serialize_product(p) for p in products]

def get_related_products(
    db: Session,
    *,
    product_id: int,
    limit: int = 8,
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")

    products = (
        db.query(Product)
        .filter(
            Product.category_id == product.category_id,
            Product.id != product_id,
        )
        .order_by(Product.id.desc())
        .limit(limit)
        .all()
    )
    return [serialize_product(p) for p in products]


def get_products_by_category(
    db: Session,
    *,
    category_id: int,
    skip: int = 0,
    limit: int = 50,
):
    category_exists = (
        db.query(Category.id)
        .filter(Category.id == category_id)
        .first()
    )
    if not category_exists:
        raise HTTPException(404, "Category not found")

    products = (
        db.query(Product)
        .filter(Product.category_id == category_id) 
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [serialize_product(p) for p in products]


def get_product_by_id(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None
    return serialize_product(product)


def get_products_by_seller(db: Session, seller_id: int):
    products = db.query(Product).filter(Product.seller_id == seller_id).all()
    return [serialize_product(p) for p in products]


def update_product(db: Session, product_id: int, data: ProductUpdate, user: User):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(404, "Product not found")

    if user.role == "SELLER" and product.seller_id != user.id:
        raise HTTPException(403, "Not allowed")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return serialize_product(product)
    

def update_product_stock(db: Session, product_id: int, seller_id: int, stock: int):
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.seller_id == seller_id
    ).first()

    if not product:
        raise HTTPException(404, "Product not found")

    product.stock = stock
    db.commit()
    db.refresh(product)
    return serialize_product(product)


def delete_product(db: Session, product_id: int, user: User):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(404, "Product not found")
    
    if user.role == "SELLER" and product.seller_id != user.id:
        raise HTTPException(403, "Not allowed")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted"}
