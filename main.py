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
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Geliştirme için "*" olabilir, prod'da sınırlı tut
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static") #static klasörünü ana app'e tanıttık

templates = Jinja2Templates(directory="templates")

app.include_router(auth_router)
app.include_router(material_router)
app.include_router(recipe_router)


Base.metadata.create_all(bind=engine) #veritabanı yoksa oluşturur -> tarifai_app.db

# app biri girerse direk logine yönlendirdik
@app.get("/", response_class=HTMLResponse)
def get_home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/home", response_class=HTMLResponse)
async def get_home(request: Request):
    # Giriş yapılmışsa anasayfaya yönlendirme
    return templates.TemplateResponse("index.html", {"request": request})

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="TarifAlJam API",
        version="1.0.0",
        description="Tarif ve kullanıcı yönetimi",
        routes=app.routes,
    )
    # Token URL'yi düzelt
    if "OAuth2PasswordBearer" in openapi_schema["components"]["securitySchemes"]:
        openapi_schema["components"]["securitySchemes"]["OAuth2PasswordBearer"]["flows"]["password"]["tokenUrl"] = "/auth/token"
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi