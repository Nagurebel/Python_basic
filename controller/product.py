from sqlalchemy.orm import Session
from model.productModel import Product, ProductCreate, ProductUpdate, ProductResponse
from schema.schema import ApiResponse


def get_all_products(db: Session) -> ApiResponse[list[ProductResponse]]:
    products = db.query(Product).all()
    response = [ProductResponse.model_validate(p) for p in products]
    return ApiResponse(
        error=False,
        message="Products found successfully",
        data=response
    )


def get_product_by_id(db: Session, product_id: int) -> ProductResponse | None:
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        return None
    return ProductResponse.model_validate(product)


def create_product(db: Session, data: ProductCreate) -> ProductResponse:
    product = Product(name=data.name, description=data.description, price=data.price)
    db.add(product)
    db.commit()
    db.refresh(product)
    return ProductResponse.model_validate(product)


def update_product(db: Session, product_id: int, data: ProductUpdate) -> ProductResponse | None:
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        return None
    if data.name is not None:
        product.name = data.name
    if data.description is not None:
        product.description = data.description
    if data.price is not None:
        product.price = data.price
    db.commit()
    db.refresh(product)
    return ProductResponse.model_validate(product)


def delete_product(db: Session, product_id: int) -> bool:
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        return False
    db.delete(product)
    db.commit()
    return True
