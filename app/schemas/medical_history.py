from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from app.core.const import ChestPainType, RestEcg, SmokingStatus, Sex
from app.schemas.medication import MedicationEntryCreate, MedicationEntryRead
from datetime import datetime


class MedicalHistoryCreate(BaseModel):
    id: str  # generado en el frontend
    age: int
    sex: Sex
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
    height: Optional[float] = None
    weight: Optional[float] = None
    body_surface_area: Optional[float] = None
    description: Optional[str] = None
    heart_disease: bool
    model_prediction: Optional[float] = None
    model_confidence: Optional[float] = None
    model_used: Optional[str] = None
    medications: List[MedicationEntryCreate] = []

    model_config = ConfigDict(from_attributes=True)


class MedicalHistoryRead(BaseModel):
    id: str
    age: int
    smoking_status: Optional[str] = None
    sedentary_lifestyle: Optional[bool] = None
    systolic_blood_pressure: Optional[float] = None
    diastolic_blood_pressure: Optional[float] = None
    ldl_cholesterol: Optional[float] = None
    max_hr: Optional[float] = None
    chest_pain_type: Optional[ChestPainType] = None
    exang: Optional[bool] = None
    fasting_blood_sugar: Optional[float] = None
    body_mass_index: Optional[float] = None
    rest_ecg: Optional[RestEcg] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    body_surface_area: Optional[float] = None
    created_at: datetime
    description: Optional[str] = None
    heart_disease: bool
    model_prediction: Optional[float] = None
    model_confidence: Optional[float] = None
    model_used: Optional[str] = None
    medications: List[MedicationEntryRead] = []

    model_config = ConfigDict(from_attributes=True)
