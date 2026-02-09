# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.db.session import SessionLocal
# from app.schemas.auth import RegisterSchema
# from app.services.auth_service import register_user, login_user

# router = APIRouter(prefix="/auth", tags=["Auth"])
 
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @router.post("/register")
# def register(data: RegisterSchema, db: Session = Depends(get_db)):
#     register_user(db, data)
#     return {"message": "Registered successfully"}

# @router.post("/login")
# def login(email: str, password: str, db: Session = Depends(get_db)):
#     result = login_user(db, email, password)
#     if not result:
#         raise HTTPException(401, "Invalid credentials")

#     token, role = result
#     return {
#         "access_token": token,
#         "token_type": "bearer",
#         "role": role
#     }




from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.auth import RegisterSchema
from app.services.auth_service import register_user, login_user

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal() 
    try:
        yield db    
    finally:
        db.close()

@router.post("/register")
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    register_user(db, data)
    return {"message": "Registered successfully"}

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):   
    result = login_user(
        db,
        email=form_data.username,   
        password=form_data.password
    )
    

    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token, role = result

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": role
    }
