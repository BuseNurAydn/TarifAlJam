from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated, List
from models import Recipe, Materials
from schemas.recipe import RecipeCreate, RecipeResponse
from services.gemini_service import generate_recipe
from datetime import datetime
from pydantic import BaseModel

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

db_dependency = Annotated[Session, Depends(get_db)]

class MaterialList(BaseModel):
    materials: List[str]

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