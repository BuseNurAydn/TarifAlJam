from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from database import SessionLocal
<<<<<<< HEAD
from typing import Annotated, List
from models import Materials
from schemas.materials import MaterialCreate, MaterialResponse
from datetime import datetime
=======
from typing import Annotated
from models import Base , Materials
from starlette import status
from pydantic import BaseModel,Field
>>>>>>> ff0c3125156651163ff1273fa1882febf018aba1

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

<<<<<<< HEAD
db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", response_model=MaterialResponse)
async def create_material(material: MaterialCreate, db: db_dependency):
    db_material = Materials(
        material_name=material.material_name,
        isExpiring=material.isExpiring,
        ExpirationDate=material.ExpirationDate
    )
=======
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
>>>>>>> ff0c3125156651163ff1273fa1882febf018aba1
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material

<<<<<<< HEAD
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
=======
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
>>>>>>> ff0c3125156651163ff1273fa1882febf018aba1
