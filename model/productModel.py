from sqlalchemy import Column, Integer, String, Float
from pydantic import BaseModel
from db_config.db import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500), default="")
    price = Column(Float, nullable=False)


class ProductCreate(BaseModel):
    name: str
    description: str = ""
    price: float


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float

    class Config:
        from_attributes = True
