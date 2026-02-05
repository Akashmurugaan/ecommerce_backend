from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models.measurement import Measurement
from app.schemas.measurement import MeasurementCreate, MeasurementOut
from app.dependencies.roles import require_roles
from app.db.models.user import User

router = APIRouter(prefix="/measurements", tags=["Measurements"])
@router.post("/", response_model=MeasurementOut)
def create_measurement(
    data: MeasurementCreate,
    db: Session = Depends(get_db),
    admin:User=Depends(require_roles("ADMIN"))
):
    if db.query(Measurement).filter(Measurement.name == data.name).first():
        raise HTTPException(400, "Measurement already exists")

    measurement = Measurement(name=data.name)
    db.add(measurement)
    db.commit()
    db.refresh(measurement)
    return measurement
@router.get("/", response_model=list[MeasurementOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Measurement).all()