

from fastapi import Depends, HTTPException, status
from app.dependencies.auth import get_current_user
from app.db.models.user import User

def require_roles(*allowed_roles: str):
    def role_checker(user: User = Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )
        return user
    return role_checker



# from fastapi import Depends, HTTPException, status
# from app.dependencies.auth import get_current_user
# from app.db.models.user import User

# def require_admin(user: User = Depends(get_current_user)):
#     if user.role != "ADMIN":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Admin access required"
#         )
#     return user

# def require_seller(user: User = Depends(get_current_user)):
#     if user.role not in ["SELLER", "ADMIN"]:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Seller access required"
#         )
#     return user
