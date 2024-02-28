from inventory_app import models, schemas
from passlib.context import CryptContext
from sqlalchemy.orm import Session

bcrypt_context = CryptContext(schemes=["bcrypt"])


def get_item(db: Session, user_id: int, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id). \
        filter(models.Item.owner_id == user_id).first()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def update_user_password(db: Session, user_id: int, hashed_password: str):
    db_user = db.query(models.User).filter(models.User.id == user_id)
    db_user.update({
        models.User.hashed_password: hashed_password
    })

    db.commit()


def get_item_by_id(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def get_item_by_name(db: Session, name: str):
    return db.query(models.Item).filter(models.Item.name == name).first()


def get_items(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Item). \
        filter(models.Item.owner_id == user_id).offset(skip).limit(limit).all()


def get_all_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int, user_id: int):
    db.query(models.Item).filter(models.Item.id == item_id). \
        filter(models.Item.owner_id == user_id).delete()
    db.commit()


def delete_item_by_id(db: Session, item_id: int):
    db.query(models.Item).filter(models.Item.id == item_id).delete()
    db.commit()


def update_item(db: Session, item_id: int, item: schemas.ItemBase):
    db_item = db.query(models.Item).filter(models.Item.id == item_id)
    db_item.update({
        models.Item.name: item.name,
        models.Item.description: item.description,
        models.Item.category: item.category,
        models.Item.quantity: item.quantity,
        models.Item.price: item.price,
    })
    db.commit()


def create_user(db: Session, user: schemas.UserCreate):
    db_item = models.User(
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=bcrypt_context.hash(user.password),
        is_active=True,
        role=user.role

    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_user_by_name(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()
