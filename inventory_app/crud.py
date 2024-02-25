from sqlalchemy.orm import Session

from . import models, schemas


def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def get_item_by_name(db: Session, name: str):
    return db.query(models.Item).filter(models.Item.name == name).first()


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int):
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