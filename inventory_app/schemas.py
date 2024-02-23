from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    description: str
    category: str
    quantity: int
    price: float


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True
