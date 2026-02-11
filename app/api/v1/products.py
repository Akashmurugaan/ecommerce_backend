# # app/api/v1/products.py
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.db.session import get_db
# from app.dependencies.roles import require_roles
# from app.db.models.product import Product
# from app.db.models.product_measurement import ProductMeasurement
# from app.db.models.measurement import Measurement
# from app.db.models.category import Category
# from app.schemas.product import ProductCreate, ProductOut
# from app.db.models.user import User
# from app.services.product_service import (
#     create_product,
#     get_all_products,
# )

# router = APIRouter(prefix="/products", tags=["Products for Sellers"])     

# @router.post("/", response_model=ProductOut)
# def add_product(
#     data: ProductCreate,
#     db: Session = Depends(get_db),
#     seller: User = Depends(require_roles("SELLER"))
#     # seller = Depends(require_roles("SELLER"))
# ):
#     category = db.query(Category).filter(Category.id == data.category_id).first()
#     if not category:
#         raise HTTPException(400, "Invalid category")

#     product = Product(
#         name=data.name,
#         description=data.description,
#         price=data.price,
#         stock=data.stock,
#         seller_id=seller.id,
#         category_id=data.category_id,
#     )

#     db.add(product)
#     db.flush()  # 🔑 important

#     for measurement_id in data.size_ids:
#         db.add(
#             ProductMeasurement(
#                 product_id=product.id,
#                 measurement_id=measurement_id
#             )
#         )

#     db.commit()
#     db.refresh(product)
#     return {
#         "name": product.name,
#         "description": product.description,
#         "category": product.category.name,
#         "size": [pm.measurement.name for pm in product.sizes],
#         "price": product.price,
#         "stock": product.stock
#     }

#     # for size_id in data.size_ids:
#     #     db.add(ProductMeasurement(
#     #         product_id=product.id,
#     #         measurement_id=size_id
#     #     ))

#     # db.commit()
    
#     # sizes = (
#     #     db.query(Measurement.name)
#     #     .join(ProductMeasurement)
#     #     .filter(ProductMeasurement.product_id == product.id)
#     #     .all()
#     # )

#     # return {
#     #     "name": product.name,
#     #     "description": product.description,
#     #     "category": category.name,
#     #     "size": [s[0] for s in sizes],
#     #     "price": product.price,
#     #     "stock": product.stock
#     # }

# @router.get("/", response_model=list[ProductOut])
# def list_products(db: Session = Depends(get_db)):
#     return get_all_products(db)



# # from fastapi import APIRouter, Depends, HTTPException
# # from sqlalchemy.orm import Session
# # from app.db.session import get_db
# # from app.schemas.product import ProductCreate, ProductOut, ProductUpdate, ProductStockUpdate
# # from app.services.product_service import (
# #     create_product,
# #     update_product,
# #     delete_product,
# #     get_all_products,
# #     get_product_by_id,
# #     get_products_by_seller,
# #     update_product_stock
# # )
# # from app.dependencies.roles import require_roles
# # from app.db.models.user import User

# # router = APIRouter(prefix="/products", tags=["Products"])


# # # 🔓 Public - anyone can view products
# # @router.get("/", response_model=list[ProductOut])
# # def list_products(db: Session = Depends(get_db)):
# #     return get_all_products(db)

# # @router.get("/my-products", response_model=list[ProductOut])
# # def get_my_products(
# #     db: Session = Depends(get_db),
# #     user=Depends(require_roles("SELLER"))
# # ):
# #     return get_products_by_seller(db, seller_id=user.id)


# # @router.patch("/{product_id}/stock", response_model=ProductOut)
# # def update_stock(
# #     product_id: int,
# #     data: ProductStockUpdate,
# #     db: Session = Depends(get_db),
# #     user = Depends(require_roles("SELLER"))
# # ):
# #     return update_product_stock(
# #         db=db,
# #         product_id=product_id,
# #         seller_id=user.id,
# #         stock=data.stock
# #     )

# # # 🔓 Public - product detail
# # @router.get("/{product_id}", response_model=ProductOut)
# # def product_detail(product_id: int, db: Session = Depends(get_db)):
# #     product = get_product_by_id(db, product_id)
# #     if not product:
# #         raise HTTPException(status_code=404, detail="Product not found")
# #     return product


# # # 🔒 Seller only - add product
# # @router.post("/", response_model=ProductOut)
# # def add_product(
# #     data: ProductCreate,
# #     db: Session = Depends(get_db),
# #     user: User = Depends(require_roles("SELLER"))
# # ):
# #     return create_product(
# #         db=db,
# #         data=data,
# #         seller_id=user.id
# #     )


# # @router.put("/{product_id}", response_model=ProductOut)
# # def update_product_api(
# #     product_id: int,
# #     data: ProductUpdate,
# #     db: Session = Depends(get_db),
# #     user: User = Depends(require_roles("SELLER", "ADMIN"))
# # ):
# #     return update_product(db, product_id, data, user)


# # @router.delete("/{product_id}")
# # def delete_product_api(
# #     product_id: int,
# #     db: Session = Depends(get_db),
# #     user: User = Depends(require_roles("SELLER", "ADMIN"))
# # ):
# #     return delete_product(db, product_id, user)






import base64
import binascii

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models.product import Product
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductOut,
    ProductStockUpdate
)
from app.services.product_service import (
    create_product,
    get_all_products,
    get_product_by_id,
    get_products_by_seller,
    set_product_image,
    update_product,
    update_product_stock,
    delete_product
)
from app.dependencies.roles import require_roles
from app.db.models.user import User

router = APIRouter(prefix="/products", tags=["Products"])

MAX_IMAGE_BYTES = 3 * 1024 * 1024  # 3MB
ALLOWED_IMAGE_MIME = {"image/jpeg", "image/png", "image/webp", "image/gif"}


# 🔓 Public
@router.get("/", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return get_all_products(db)
@router.get("/my-products", response_model=list[ProductOut])
def my_products(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("SELLER"))
):
    return get_products_by_seller(db, user.id)              

@router.get("/{product_id}", response_model=ProductOut)
def product_detail(product_id: int, db: Session = Depends(get_db)):
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    return product


# 🔒 Seller
@router.post("/", response_model=ProductOut)
def add_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("SELLER"))
):
    return create_product(db, data, user.id)




@router.put("/{product_id}", response_model=ProductOut)
def update_product_api(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("SELLER", "ADMIN"))
):
    return update_product(db, product_id, data, user)


@router.patch("/{product_id}/stock", response_model=ProductOut)
def update_stock(
    product_id: int,
    data: ProductStockUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("SELLER"))
):
    return update_product_stock(db, product_id, user.id, data.stock)


@router.delete("/{product_id}")
def delete_product_api(
    product_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("SELLER", "ADMIN"))
):
    return delete_product(db, product_id, user)


@router.post("/{product_id}/image", response_model=ProductOut)
def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("SELLER", "ADMIN")),
):
    if file.content_type and file.content_type not in ALLOWED_IMAGE_MIME:
        raise HTTPException(400, "Unsupported image type")

    content = file.file.read()
    if not content:
        raise HTTPException(400, "Empty file")
    if len(content) > MAX_IMAGE_BYTES:
        raise HTTPException(413, "Image too large")

    image_b64 = base64.b64encode(content).decode("ascii")

    return set_product_image(
        db,
        product_id,
        user,
        image_base64=image_b64,
        image_mime=file.content_type,
        image_filename=file.filename,
    )


@router.get("/{product_id}/image")
def get_product_image(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product or not product.image_base64:
        raise HTTPException(404, "Image not found")

    try:
        raw = base64.b64decode(product.image_base64, validate=True)
    except (binascii.Error, ValueError):
        raise HTTPException(500, "Stored image is corrupted")

    headers = {"Cache-Control": "public, max-age=3600"}
    if product.image_filename:
        headers["Content-Disposition"] = f'inline; filename="{product.image_filename}"'

    return Response(
        content=raw,
        media_type=product.image_mime or "application/octet-stream",
        headers=headers,
    )
