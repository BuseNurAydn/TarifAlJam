from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated, List
from models import Materials
from schemas.materials import MaterialCreate, MaterialResponse
from datetime import datetime

router = APIRouter(
    prefix="/materials",
    tags=["materials"]
)

# DB bağlantısı
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", response_model=MaterialResponse)
async def create_material(material: MaterialCreate, db: db_dependency):
    db_material = Materials(
        material_name=material.material_name,
        isExpiring=material.isExpiring,
        ExpirationDate=material.ExpirationDate
    )
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material

@router.get("/", response_model=List[MaterialResponse])
async def get_materials(db: db_dependency):
    materials = db.query(Materials).all()
    return materials

@router.get("/{material_id}", response_model=MaterialResponse)
async def get_material(material_id: int, db: db_dependency):
    material = db.query(Materials).filter(Materials.id == material_id).first()
    if material is None:
        raise HTTPException(status_code=404, detail="Malzeme bulunamadı")
    return material

@router.put("/{material_id}", response_model=MaterialResponse)
async def update_material(material_id: int, material: MaterialCreate, db: db_dependency):
    db_material = db.query(Materials).filter(Materials.id == material_id).first()
    if db_material is None:
        raise HTTPException(status_code=404, detail="Malzeme bulunamadı")
    
    db_material.material_name = material.material_name
    db_material.isExpiring = material.isExpiring
    db_material.ExpirationDate = material.ExpirationDate
    
    db.commit()
    db.refresh(db_material)
    return db_material

@router.delete("/{material_id}")
async def delete_material(material_id: int, db: db_dependency):
    db_material = db.query(Materials).filter(Materials.id == material_id).first()
    if db_material is None:
        raise HTTPException(status_code=404, detail="Malzeme bulunamadı")
    
    db.delete(db_material)
    db.commit()
    return {"message": "Malzeme başarıyla silindi"}
