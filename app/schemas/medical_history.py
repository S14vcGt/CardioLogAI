from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class MedicalHistoryCreate(BaseModel):
    smoking_status: str
    sedentary_lifestyle: bool
    blood_pressure: int
    ldl_cholesterol: int
    fasting_blood_sugar: Optional[int]
    body_mass_index: Optional[float]
    recg: str
    height: float
    weight: float
    body_surface_area: Optional[float]
    description: Optional[str]
    diabetes: Optional[bool]
    heart_disease: Optional[bool]

    model_config = ConfigDict(from_attributes=True)


class MedicalHistoryRead(BaseModel):
    id: str
    age: int
    smoking_status: str
    sedentary_lifestyle: bool
    blood_pressure: int
    ldl_cholesterol: int
    fasting_blood_sugar: int
    body_mass_index: float
    recg: str
    height: float
    weight: float
    body_surface_area: float
    created_at: datetime
    description: str
    diabetes: bool
    heart_disease: bool

    model_config = ConfigDict(from_attributes=True)
