from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.models.patient import Patient

class MedicalHistory(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    age: int 
    smoking_status: str
    sedentary_lifestyle: bool
    blood_pressure: int
    ldl_cholesterol: int
    fasting_blood_sugar: int
    body_mass_index: float
    recg: str #resting electrocardiogram
    height:float
    weight: float
    body_surface_area:float
    date: datetime = Field(default_factory=datetime.now())
    description: str
    patient_id: str = Field(foreign_key="patient.id")
    patient: Optional["Patient"] = Relationship(back_populates="medical_histories") 