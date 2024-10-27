from .base import Base


class Brand(Base, table=True):
    __tablename__ = "brands"

    name: str
