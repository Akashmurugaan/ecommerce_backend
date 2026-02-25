from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies.roles import require_roles
from app.db.models.user import User
from app.schemas.address import AddressCreate, AddressOut, AddressUpdate
from app.services.address_service import (
    create_address,
    delete_address,
    list_addresses,
    set_default_address,
    update_address,
)

router = APIRouter(prefix="/addresses", tags=["Addresses"])

@router.get("/", response_model=list[AddressOut])
def my_addresses(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("USER")),
):
    return list_addresses(db, user_id=user.id)


@router.post("/", response_model=AddressOut)
def add_address(
    data: AddressCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("USER")),
):
    return create_address(db, user_id=user.id, data=data)


@router.put("/{address_id}", response_model=AddressOut)
def edit_address(
    address_id: int,
    data: AddressUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("USER")),
):
    return update_address(db, user_id=user.id, address_id=address_id, data=data)


@router.post("/{address_id}/default", response_model=AddressOut)
def make_default(
    address_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("USER")),
):
    return set_default_address(db, user_id=user.id, address_id=address_id)


@router.delete("/{address_id}")
def remove_address(
    address_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("USER")),
):
    return delete_address(db, user_id=user.id, address_id=address_id)

