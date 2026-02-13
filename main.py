from fastapi import FastAPI, APIRouter
from db_config.db import engine
from model.productModel import Product
from db_config.db import Base
from routers.productRoute import router as product_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

router = APIRouter()

global_router = APIRouter( prefix="/demo")

global_router.include_router(product_router, prefix="/products")

app.include_router(global_router)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)