from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from inventory_app import crud, schemas
from inventory_app.database import SessionLocal
from inventory_app.routers.auth import get_current_user
from passlib.context import CryptContext
from sqlalchemy.orm import Session

router = APIRouter(prefix="/user",
                   tags=["user"])
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=schemas.User)
def get_user(user: user_dependency, db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    db_user = crud.get_user(db, user_id=user.get("id"))
    return db_user


@router.put("/password")
def change_password(user: user_dependency,
                    user_verification: schemas.UserVerification,
                    db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    db_user = crud.get_user(db, user_id=user.get("id"))
    if not bcrypt_context.verify(user_verification.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Error on password change")
    hashed_password = bcrypt_context.hash(user_verification.new_password)
    crud.update_user_password(db, user_id=user.get("id"), hashed_password=hashed_password)
