from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MaterialCreate(BaseModel):
    materials_name: str
    isExpiring: Optional[bool] = False
    ExpirationDate: Optional[datetime] = None


class MaterialResponse(MaterialCreate):
    id: int

    class Config:
        orm_mode = True
