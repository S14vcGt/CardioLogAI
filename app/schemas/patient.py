from typing import Optional
from pydantic import BaseModel
from datetime import date

class PatientCreate(BaseModel):
    name: str
    birth_date: date

class PatientRead(BaseModel):
    id: int
    name: str
    birth_date: date
    class Config:
        orm_mode = True 