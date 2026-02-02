from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models.user import User
from app.core.security import hash_password, verify_password, create_access_token

def register_user(db: Session, data):
    user = User(
        name=data.name,
        email=data.email,
        phone=data.phone,
        password_hash=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    return user

# def login_user(db: Session, email: str, password: str):
#     user = db.query(User).filter(User.email == email).first()
#     if not user or not verify_password(password, user.password_hash):
#         return None

#     token = create_access_token({"user_id": user.id, "role": user.role})
#     return token, user.role


def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password_hash):
        return None
    if not user.is_active:
        raise HTTPException(403, "User is blocked")

    token = create_access_token({
        "sub": str(user.id),   
        "role": user.role
    })

    return token, user.role