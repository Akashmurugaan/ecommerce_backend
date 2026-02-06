# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.db.session import get_db
# from app.schemas.measurement import MeasurementBulkCreate, MeasurementOut
# from app.dependencies.roles import require_roles
# from app.services.measurement_service import bulk_create_measurements
# from app.db.models.user import User
# from app.db.models.category import Category

# router = APIRouter(prefix="/measurements", tags=["Measurements"])

# @router.post("/bulk", response_model=list[MeasurementOut])
# def add_measurements_bulk(
#     data: MeasurementBulkCreate,
#     db: Session = Depends(get_db),
#     seller: User = Depends(require_roles("SELLER"))
# ):
#     category = db.query(Category).filter(Category.id == data.category_id).first()
#     if not category:
#         raise HTTPException(404, "Category not found")
    
#     try:
#         return bulk_create_measurements(
#             db=db,
#             seller_id=seller.id,
#             category_id=data.category_id,
#             measurements=data.measurements
#         )
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))





# # from fastapi import APIRouter, Depends, HTTPException
# # from sqlalchemy.orm import Session

# # from app.db.session import get_db
# # from app.schemas.measurement import MeasurementCreate, MeasurementOut
# # from app.dependencies.roles import require_roles
# # from app.services.measurement_service import (
# #     create_measurement as create_measurement_service,
# #     get_my_measurements
# # )
# # from app.db.models.user import User

# # router = APIRouter(
# #     prefix="/measurements",
# #     tags=["Measurements"]
# # )

# # # ➕ Seller adds size
# # @router.post("/", response_model=MeasurementOut)
# # def add_measurement(
# #     data: MeasurementCreate,
# #     db: Session = Depends(get_db),
# #     seller: User = Depends(require_roles("SELLER"))
# # ):
# #     try:
# #         return create_measurement_service(
# #             db=db,
# #             name=data.name,
# #             seller_id=seller.id
# #         )
# #     except ValueError as e:
# #         raise HTTPException(status_code=400, detail=str(e))


# # # 📄 Seller views their sizes
# # @router.get("/my", response_model=list[MeasurementOut])
# # def my_measurements(
# #     db: Session = Depends(get_db),
# #     seller: User = Depends(require_roles("SELLER"))
# # ):
# #     return get_my_measurements(db, seller.id)


# app/api/v1/measurements.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies.roles import require_roles
from app.schemas.measurement import MeasurementCreate, MeasurementOut
from app.services.measurement_service import create_measurement
from app.db.models.measurement import Measurement
from app.db.models.user import User

router = APIRouter(prefix="/measurements", tags=["Measurements"])

@router.post("/", response_model=MeasurementOut)
def add_measurement(
    data: MeasurementCreate,
    db: Session = Depends(get_db),
    seller: User = Depends(require_roles("SELLER"))
):
    return create_measurement(
        db=db,
        seller_id=seller.id,
        category_id=data.category_id,
        name=data.name
    )
@router.get("/by-category/{category_id}", response_model=list[MeasurementOut])
def get_measurements_by_category(
    category_id: int,
    db: Session = Depends(get_db),
    seller: User = Depends(require_roles("SELLER"))
):
    return db.query(Measurement).filter(
        Measurement.category_id == category_id,
        Measurement.seller_id == seller.id
    ).all()
