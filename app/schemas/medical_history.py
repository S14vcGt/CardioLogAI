from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class MedicalHistoryCreate(BaseModel):
    smoking_status: str
    sedentary_lifestyle: bool
    blood_pressure: int
    ldl_cholesterol: int
    fasting_blood_sugar: int
    body_mass_index: float
    recg: str
    height:float
    weight: float
    body_surface_area:float
    date: datetime
    description: str
    patient_id: str

class MedicalHistoryRead(BaseModel):
    id: int
    age: int 
    smoking_status: str
    sedentary_lifestyle: bool
    blood_pressure: int
    ldl_cholesterol: int
    fasting_blood_sugar: int
    body_mass_index: float
    recg: str
    height:float
    weight: float
    body_surface_area:float
    date: datetime = Field(default_factory=datetime.now())
    description: str
    class Config:
        from_attributes = True 