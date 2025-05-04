from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class RecipeCreate(BaseModel):
    title: str
    description: Optional[str] = None
    instructions: str
    materials: List[str]

class RecipeResponse(RecipeCreate):
    id: int
    created_by: int
    created_at: datetime

    class Config:
        orm_mode = True 