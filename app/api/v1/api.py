from fastapi import APIRouter
from app.api.v1 import auth, measurements, products, admin, categories, user

api_router = APIRouter()
# api_router.include_router(health.router, tags=["health"])
# api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(profile.router, tags=["profile"])
# api_router.include_router(categories.router, tags=["categories"])
# api_router.include_router(transactions.router, tags=["transactions"])
api_router.include_router(auth.router, prefix="/api/v1")
api_router.include_router(products.router, prefix="/api/v1")
api_router.include_router(admin.router, prefix="/api/v1")
api_router.include_router(categories.router, prefix="/api/v1")
api_router.include_router(measurements.router, prefix="/api/v1")
api_router.include_router(user.router, prefix="/api/v1")
