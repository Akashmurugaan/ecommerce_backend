from fastapi import FastAPI
# from app.api.v1 import auth, products
from app.api.v1.api import api_router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="E-Commerce API")
app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to Ecommerce API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



