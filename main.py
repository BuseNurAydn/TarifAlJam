from fastapi import FastAPI

from models import Base
from database import engine

from routers.auth import router as auth_router
from routers.materials import router as material_router
from routers.recipe import  router as recipe_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(material_router)
app.include_router(recipe_router)

Base.metadata.create_all(bind=engine) #veritabanı yoksa oluşturur -> tarifai_app.db