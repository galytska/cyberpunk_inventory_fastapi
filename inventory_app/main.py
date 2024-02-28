from fastapi import FastAPI
from inventory_app import models
from inventory_app.database import engine
from inventory_app.routers import admin, auth, items, users

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(items.router)
app.include_router(users.router)
