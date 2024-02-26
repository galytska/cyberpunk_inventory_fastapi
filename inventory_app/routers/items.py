from fastapi import APIRouter, Depends, HTTPException, status
from inventory_app import crud, schemas
from inventory_app.database import SessionLocal
from sqlalchemy.orm import Session

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = crud.get_item_by_name(db, name=item.name)
    if db_item:
        raise HTTPException(status_code=400, detail="Item with such name already registered")
    return crud.create_item(db=db, item=item)


@router.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    crud.delete_item(db=db, item_id=item_id)


@router.put("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_item(item_id: int, item: schemas.ItemBase, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    crud.update_item(db=db, item_id=item_id, item=item)
