from fastapi import FastAPI
from inventory_app import models
from inventory_app.database import engine
from inventory_app.routers.items import router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)
