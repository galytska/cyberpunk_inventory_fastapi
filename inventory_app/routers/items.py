from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from inventory_app import crud, schemas
from inventory_app.database import SessionLocal
from inventory_app.routers.auth import get_current_user
from sqlalchemy.orm import Session

router = APIRouter(tags=["items"])
user_dependency = Annotated[dict, Depends(get_current_user)]


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/items/", response_model=schemas.Item)
def create_item(user: user_dependency, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    db_item = crud.get_item_by_name(db, name=item.name)
    if db_item:
        raise HTTPException(status_code=400, detail="Item with such name already registered")
    return crud.create_item(db=db, item=item, user_id=user.get("id"))


@router.get("/items/{item_id}", response_model=schemas.Item)
def read_item(user: user_dependency, item_id: int, db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    db_item = crud.get_item(db, user_id=user.get("id"), item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.get("/items/", response_model=list[schemas.Item])
def read_items(user: user_dependency,
               skip: int = 0,
               limit: int = 100,
               db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    items = crud.get_items(db, user_id=user.get("id"), skip=skip, limit=limit)
    return items


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(user: user_dependency,
                item_id: int,
                db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    db_item = crud.get_item(db, user_id=user.get("id"), item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    crud.delete_item(db=db, item_id=item_id, user_id=user.get("id"))


@router.put("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_item(user: user_dependency,
                item_id: int,
                item: schemas.ItemBase,
                db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    db_item = crud.get_item(db, user_id=user.get("id"), item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    crud.update_item(db=db, item_id=item_id, item=item)
