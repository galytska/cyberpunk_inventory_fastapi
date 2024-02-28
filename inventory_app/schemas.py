from pydantic import BaseModel, Field


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
    owner_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    role: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    hashed_password: str

    class Config:
        from_attributes = True


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


class Token(BaseModel):
    access_token: str
    token_type: str
