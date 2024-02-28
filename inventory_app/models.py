from inventory_app.database import Base
from sqlalchemy import TEXT, Boolean, Column, Float, ForeignKey, Integer, String


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(TEXT, index=True)
    category = Column(String, index=True)
    quantity = Column(Integer)
    price = Column(Float)
    owner_id = Column(Integer, ForeignKey("users.id"))


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
