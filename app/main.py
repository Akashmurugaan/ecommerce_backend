from fastapi import FastAPI
from app.api.v1 import auth, products

app = FastAPI(title="E-Commerce API")

app.include_router(auth.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")
