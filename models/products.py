from sqlmodel import Field
from .base import Base


class Product(Base, table=True):
    __tablename__ = "products"

    title: str
    price: float
    description: str = None
    image: str = None
    category_id: int | None = Field(default=None, foreign_key="categories.id")
