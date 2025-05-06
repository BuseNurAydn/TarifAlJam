from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated, List
from models import Recipe, Materials
from schemas.recipe import RecipeCreate, RecipeResponse
from services.gemini_service import generate_recipe
from datetime import datetime
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/recipes",
    tags=["recipes"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

templates = Jinja2Templates(directory="templates")
db_dependency = Annotated[Session, Depends(get_db)]

class MaterialList(BaseModel):
    materials: List[str]

@router.get("/recipe-page")
def render_recipe_page(request: Request):
    return templates.TemplateResponse("recipes.html", {"request": request})

@router.post("/generate", response_model=RecipeResponse)
async def create_recipe_with_ai(material_list: MaterialList, db: db_dependency):
    try:
        # Gemini API ile tarif oluştur
        generated_recipe = generate_recipe(material_list.materials)
        
        # Veritabanına kaydet
        db_recipe = Recipe(
            title=generated_recipe["title"],
            description=generated_recipe["description"],
            instructions=generated_recipe["instructions"],
            created_by=1,  # TODO: Gerçek kullanıcı ID'sini ekle
            created_at=datetime.now()
        )
        
        # Malzemeleri ekle
        for material_name in material_list.materials:
            material = db.query(Materials).filter(Materials.material_name == material_name).first()
            if material:
                db_recipe.materials.append(material)
        
        db.add(db_recipe)
        db.commit()
        db.refresh(db_recipe)
        
        return db_recipe
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tarif oluşturulurken bir hata oluştu: {str(e)}")

@router.get("/", response_model=List[RecipeResponse])
async def get_recipes(db: db_dependency):
   
    recipes = db.query(Recipe).all()
    return recipes

@router.get("/{recipe_id}", response_model=RecipeResponse)
async def get_recipe(recipe_id: int, db: db_dependency):
   
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Tarif bulunamadı")
    return recipe

@router.get("/search/{keyword}", response_model=List[RecipeResponse])
async def search_recipes(keyword: str, db: db_dependency):
   
    recipes = db.query(Recipe).filter(
        (Recipe.title.ilike(f"%{keyword}%")) | 
        (Recipe.description.ilike(f"%{keyword}%"))
    ).all()
    return recipes

@router.get("/by-material/{material_name}", response_model=List[RecipeResponse])
async def get_recipes_by_material(material_name: str, db: db_dependency):
   
    material = db.query(Materials).filter(Materials.material_name == material_name).first()
    if material is None:
        raise HTTPException(status_code=404, detail="Malzeme bulunamadı")
    
    recipes = material.recipes
    return recipes