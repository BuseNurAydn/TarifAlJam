from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)
def get_db():  #Bu fonksiyon bize veritabanını veriyor
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]  #Dependency Injection
