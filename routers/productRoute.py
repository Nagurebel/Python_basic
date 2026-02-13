from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db_config.db import get_db
from model.productModel import ProductCreate, ProductUpdate, ProductResponse
from controller import product as product_controller
from schema.schema import ApiResponse

router = APIRouter( tags=["products"])


@router.get("/", response_model=ApiResponse[list[ProductResponse]])
def list_products(db: Session = Depends(get_db)):
    return product_controller.get_all_products(db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    result = product_controller.get_product_by_id(db, product_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return result


@router.post("/", response_model=ProductResponse)
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    return product_controller.create_product(db, data)


@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, data: ProductUpdate, db: Session = Depends(get_db)):
    result = product_controller.update_product(db, product_id, data)
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return result


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    ok = product_controller.delete_product(db, product_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted"}
