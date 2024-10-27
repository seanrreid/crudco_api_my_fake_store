from .base import Base


class Category(Base, table=True):
    __tablename__ = "categories"

    name: str
