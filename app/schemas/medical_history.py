from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class MedicalHistoryCreate(BaseModel):
    description: str

class MedicalHistoryRead(BaseModel):
    id: int
    date: datetime
    description: str
    class Config:
        orm_mode = True 