from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated
from models import Base , Materials
from starlette import status
from pydantic import BaseModel,Field

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

#request body
class MaterialRequest(BaseModel):
    material_name: str = Field(min_length=3)
    isExpiring: bool
    expirationDate: str = Field(gt=0, lt=20)

db_dependency = Annotated[Session, Depends(get_db)]  # Dependency Injection

def get_materials(db: db_dependency):
    return db.query(Materials).all()

def create_material(db: db_dependency, material: MaterialRequest):
    db_material = Materials(**material.dict())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material

def delete_material(db: db_dependency, material_id: int):
    material = db.query(Materials).filter(Materials.id == material_id).first()
    if material:
        db.delete(material)
        db.commit()
        return True
    return False

@router.get("/")
def list_materials(db: db_dependency):
    return get_materials(db)

@router.post("/")
def add_material(material: MaterialRequest, db: db_dependency):
    return create_material(db, material)

@router.delete("/{material_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_material(material_id: int, db: db_dependency):
    success = delete_material(db, material_id)
    if not success:
        raise HTTPException(status_code=404, detail="Material not found")
