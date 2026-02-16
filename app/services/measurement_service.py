# from sqlalchemy.orm import Session
# from app.db.models.measurement import Measurement

# def create_measurement(db: Session, name: str, seller_id: int):
#     exists = db.query(Measurement).filter(
#         Measurement.name == name,
#         Measurement.seller_id == seller_id
#     ).first()

#     if exists:
#         raise ValueError("Size already exists")

#     size = Measurement(name=name, seller_id=seller_id)
#     db.add(size)
#     db.commit()
#     db.refresh(size)
#     return size

# def get_my_measurements(db: Session, seller_id: int):
#     return db.query(Measurement).filter(
#         Measurement.seller_id == seller_id
#     ).all()



# app/services/measurement_service.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models.measurement import Measurement

def create_measurement(
    db: Session,
    seller_id: int,
    category_id: int,
    name: str
):
    exists = db.query(Measurement).filter(
        Measurement.name == name,
        Measurement.seller_id == seller_id,
        Measurement.category_id == category_id
    ).first()

    if exists:
        raise HTTPException(
            status_code=400,
            detail="Measurement already exists for this category"
        )

    measurement = Measurement(
        name=name,
        seller_id=seller_id,
        category_id=category_id
    )

    db.add(measurement)
    db.commit()
    db.refresh(measurement)
    return measurement

