# app/api/v1/test.py

from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/test", tags=["Test"])

@router.get("/me")
def my_profile(user=Depends(get_current_user)):
    return user
