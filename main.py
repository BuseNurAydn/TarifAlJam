from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from fastapi.staticfiles import StaticFiles
from models import Base
from database import engine
from routers.auth import router as auth_router
from routers.materials import router as material_router
from routers.recipe import router as recipe_router

app = FastAPI()

# Static ve templates klasörleri
script_dir = os.path.dirname(__file__)
st_abs_file_path = os.path.join(script_dir, "static")
app.mount("/static", StaticFiles(directory=st_abs_file_path), name="static")

templates = Jinja2Templates(directory="templates")


app.include_router(auth_router)
app.include_router(material_router)
app.include_router(recipe_router)

Base.metadata.create_all(bind=engine) #veritabanı yoksa oluşturur -> tarifai_app.db


# Ana sayfa
@app.get("/", response_class=HTMLResponse)
def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})