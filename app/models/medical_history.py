from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from uuid import uuid4
from app.Scripts.general_helpers import get_vzla_datetime
from datetime import datetime


if TYPE_CHECKING:
    from app.models.patient import Patient


class MedicalHistory(SQLModel, table=True):
    id: Optional[str] = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        description="Identificador único del historial médico",
    )
    age: int = Field(nullable=True, description="Edad del paciente")
    smoking_status: str = Field(nullable=True, description="Regularidad con la que el paciente fuma")
    sedentary_lifestyle: bool = Field(nullable=True, description="Actividad física regular")
    blood_pressure: float = Field(nullable=True, description="Presión arterial en reposo (en mm Hg)")
    ldl_cholesterol: float = Field(nullable=True, description="Colesterol sérico en mg/d")
    max_hr: float = Field(nullable=True, description="Maximo ritmo cardiaco alcanzado")
    fasting_blood_sugar: float = Field(nullable=True, description="Azúcar en sangre en ayunas (indicador de diabetes)")
    body_mass_index: float = Field(nullable=True, description="Indice de masa corporal")
    rest_ecg: str = Field(nullable=True, description="Electrocardiograma en descanso")
    weight: float = Field(nullable=True, description="Peso en Kilogramos")
    height: float = Field(nullable=True, description="Altura en Centímetros")
    body_surface_area: float = Field(nullable=True, description="Area de superficie corporal")
    heart_disease: bool = Field(description="Diagnostico de enfermedades cardiacas")
    model_prediction: float = Field(nullable=True, description="Predicción del modelo")
    created_at: datetime = Field(default_factory=get_vzla_datetime)
    description: str = Field(nullable=True, description="Descripción del historial médico")
    patient_id: str = Field(
        foreign_key="patient.id",
        description="Identificador del paciente al que pertenece el historial médico",
    )
    patient: Optional["Patient"] = Relationship(back_populates="medical_histories")
