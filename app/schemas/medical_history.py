from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.core.const import ChestPainType, RestEcg, SmokingStatus
from datetime import datetime


class MedicalHistoryCreate(BaseModel):
    age: int
    smoking_status: Optional[SmokingStatus] = None
    sedentary_lifestyle: Optional[bool] = None
    systolic_blood_pressure: Optional[float] = None
    diastolic_blood_pressure: Optional[float] = None
    ldl_cholesterol: Optional[float] = None
    max_hr: Optional[float] = None
    fasting_blood_sugar: Optional[float] = None
    chest_pain_type: Optional[ChestPainType] = None
    exang: Optional[bool] = None
    body_mass_index: Optional[float] = None
    rest_ecg: Optional[RestEcg] = None
    height: Optional[float]
    weight: Optional[float]
    body_surface_area: Optional[float]
    description: Optional[str]
    heart_disease: bool

    model_config = ConfigDict(from_attributes=True)


class MedicalHistoryRead(BaseModel):
    id: str
    age: int
    smoking_status: Optional[str]
    sedentary_lifestyle: Optional[bool]
    systolic_blood_pressure: Optional[float]
    diastolic_blood_pressure: Optional[float]
    ldl_cholesterol: Optional[float]
    max_hr: Optional[float]
    chest_pain_type: Optional[ChestPainType]
    exang: Optional[bool]
    fasting_blood_sugar: Optional[float]
    body_mass_index: Optional[float]
    rest_ecg: Optional[RestEcg]
    height: Optional[float]
    weight: Optional[float]
    body_surface_area: Optional[float]
    created_at: datetime
    description: Optional[str]
    heart_disease: bool

    model_config = ConfigDict(from_attributes=True)
