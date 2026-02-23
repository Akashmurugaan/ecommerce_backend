from fastapi import HTTPException
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import Session

from app.db.models.address import Address
from app.schemas.address import AddressCreate, AddressUpdate


def list_addresses(db: Session, *, user_id: int):
    try:
        return (
            db.query(Address)
            .filter(Address.user_id == user_id)
            .order_by(Address.is_default.desc(), Address.id.desc())
            .all()
        )
    except ProgrammingError as exc:
        msg = str(getattr(exc, "orig", exc))
        if "relation" in msg and "addresses" in msg and "does not exist" in msg:
            raise HTTPException(500, "Database not migrated. Run: alembic upgrade head")
        raise


def create_address(db: Session, *, user_id: int, data: AddressCreate, commit: bool = True):
    try:
        has_any = db.query(Address.id).filter(Address.user_id == user_id).first()
    except ProgrammingError as exc:
        msg = str(getattr(exc, "orig", exc))
        if "relation" in msg and "addresses" in msg and "does not exist" in msg:
            raise HTTPException(500, "Database not migrated. Run: alembic upgrade head")
        raise
    make_default = data.is_default or not has_any

    if make_default:
        try:
            db.query(Address).filter(Address.user_id == user_id).update(
                {"is_default": False}
            )
        except ProgrammingError as exc:
            msg = str(getattr(exc, "orig", exc))
            if "relation" in msg and "addresses" in msg and "does not exist" in msg:
                raise HTTPException(500, "Database not migrated. Run: alembic upgrade head")
            raise

    address = Address(
        user_id=user_id,
        full_name=data.full_name,
        phone=data.phone,
        line1=data.line1,
        line2=data.line2,
        city=data.city,
        state=data.state,
        postal_code=data.postal_code,
        country=data.country,
        is_default=make_default,
    )
    db.add(address)
    if commit:
        db.commit()
        db.refresh(address)
    else:
        db.flush()
    return address


def set_default_address(db: Session, *, user_id: int, address_id: int):
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

    try:
        db.query(Address).filter(Address.user_id == user_id).update(
            {"is_default": False}
        )
    except ProgrammingError as exc:
        msg = str(getattr(exc, "orig", exc))
        if "relation" in msg and "addresses" in msg and "does not exist" in msg:
            raise HTTPException(500, "Database not migrated. Run: alembic upgrade head")
        raise
    address.is_default = True
    db.commit()
    db.refresh(address)
    return address


def update_address(db: Session, *, user_id: int, address_id: int, data: AddressUpdate):
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

    for key, value in data.dict(exclude_unset=True).items():
        setattr(address, key, value)

    db.commit()
    db.refresh(address)
    return address


def delete_address(db: Session, *, user_id: int, address_id: int):
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

    was_default = bool(address.is_default)
    db.delete(address)
    db.commit()

    if was_default:
        try:
            next_address = (
                db.query(Address)
                .filter(Address.user_id == user_id)
                .order_by(Address.id.desc())
                .first()
            )
        except ProgrammingError as exc:
            msg = str(getattr(exc, "orig", exc))
            if "relation" in msg and "addresses" in msg and "does not exist" in msg:
                raise HTTPException(500, "Database not migrated. Run: alembic upgrade head")
            raise
        if next_address:
            next_address.is_default = True
            db.commit()

    return {"message": "Address deleted"}
