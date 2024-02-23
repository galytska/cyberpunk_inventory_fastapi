from sqlalchemy import TEXT, Column, Float, Integer, String

from .database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(TEXT, index=True)
    category = Column(String, index=True)
    quantity = Column(Integer)
    price = Column(Float)
