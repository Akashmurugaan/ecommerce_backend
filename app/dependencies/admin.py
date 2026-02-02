# app/dependencies/admin.py

from fastapi import Depends, HTTPException, status
from app.dependencies.auth import get_current_user
from app.db.models.user import User

def admin_required(user=Depends(get_current_user)):
    if user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access only"
        )
    return user
