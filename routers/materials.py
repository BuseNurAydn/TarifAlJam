from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated

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

db_dependency = Annotated[Session, Depends(get_db)]  #Dependency Injection
