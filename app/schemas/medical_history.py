from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class MedicalHistoryCreate(BaseModel):
    smoking_status: str
    sedentary_lifestyle: bool
    blood_pressure: float
    ldl_cholesterol: float
    max_hr: float
    fasting_blood_sugar: Optional[float]
    body_mass_index: Optional[float]
    rest_ecg: str
    height: float
    weight: float
    body_surface_area: Optional[float]
    description: Optional[str]
    heart_disease: Optional[bool]

    model_config = ConfigDict(from_attributes=True)


class MedicalHistoryRead(BaseModel):
    id: str
    age: int
    smoking_status: str
    sedentary_lifestyle: bool
    blood_pressure: float
    ldl_cholesterol: float
    max_hr: float
    fasting_blood_sugar: float
    body_mass_index: float
    rest_ecg: str
    height: float
    weight: float
    body_surface_area: float
    created_at: datetime
    description: str
    heart_disease: bool

    model_config = ConfigDict(from_attributes=True)
