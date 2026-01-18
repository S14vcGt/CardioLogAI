from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import date

class PatientCreate(BaseModel):
    name: str
    lastname: str
    birth_date: str
    address:str
    cedula: int
    phone: str
    email:str
    sex: str
    family_history: bool

class PatientRead(BaseModel):
    id: int
    name: str
    lastname: str
    birth_date: str
    address:str
    cedula: int
    phone: str
    email:str
    
    model_config = ConfigDict(from_attributes=True) 