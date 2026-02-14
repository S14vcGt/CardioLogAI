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
    age: int = Field(description="Edad del paciente")
    smoking_status: str = Field(description="Regularidad con la que el paciente fuma")
    sedentary_lifestyle: bool = Field(description="Actividad física regular")
    blood_pressure: float = Field(description="Presión arterial en reposo (en mm Hg)")
    ldl_cholesterol: float = Field(description="Colesterol sérico en mg/d")
    fasting_blood_sugar: float = Field(description="Azúcar en sangre en ayunas")
    body_mass_index: float = Field(description="Indice de masa corporal")
    recg: str = Field(description="Electrocardiograma en descanso")
    weight: float = Field(description="Peso en Kilogramos")
    height: float = Field(description="Altura en Centímetros")
    body_surface_area: float = Field(description="Area de superficie corporal")
    heart_disease: bool = Field(description="Diagnostico de enfermedades cardiacas")
    diabetes: bool = Field(description="Diagnostico de diabetes")
    created_at: datetime = Field(default_factory=get_vzla_datetime())
    description: str = Field(description="Descripción del historial médico")
    patient_id: str = Field(
        foreign_key="patient.id",
        description="Identificador del paciente al que pertenece el historial médico",
    )
    patient: Optional["Patient"] = Relationship(back_populates="medical_histories")
