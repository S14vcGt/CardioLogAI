from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import DateTime
from typing import Optional, TYPE_CHECKING
from uuid import uuid4
from app.Scripts.general_helpers import get_vzla_datetime
from app.core.const import ChestPainType, RestEcg, SmokingStatus
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
    smoking_status: SmokingStatus = Field(nullable=True, description="Regularidad con la que el paciente fuma")
    sedentary_lifestyle: bool = Field(nullable=True, description="Actividad física regular")
    systolic_blood_pressure: float = Field(nullable=True, description="Presión arterial sistólica en reposo (en mm Hg)")
    diastolic_blood_pressure: float = Field(nullable=True, description="Presión arterial diastólica en reposo (en mm Hg)")
    ldl_cholesterol: float = Field(nullable=True, description="Colesterol sérico en mg/d")
    max_hr: float = Field(nullable=True, description="Maximo ritmo cardiaco alcanzado")
    chest_pain_type: ChestPainType = Field(nullable=True, description="Tipo de dolor en el pecho")
    exang: bool = Field(nullable=True, description="Angina inducida por el ejercicio")
    fasting_blood_sugar: float = Field(nullable=True, description="Azúcar en sangre en ayunas (indicador de diabetes)")
    body_mass_index: float = Field(nullable=True, description="Indice de masa corporal")
    rest_ecg: RestEcg = Field(nullable=True, description="Electrocardiograma en descanso")
    weight: float = Field(nullable=True, description="Peso en Kilogramos")
    height: float = Field(nullable=True, description="Altura en Centímetros")
    body_surface_area: float = Field(nullable=True, description="Area de superficie corporal")
    heart_disease: bool = Field(description="Diagnostico de enfermedades cardiacas")
    model_prediction: float = Field(nullable=True, description="Predicción del modelo")
    model_accuracy: float = Field(nullable=True, description="Confianza en la predicción del modelo")
    model_used: str = Field(nullable=True, description="Modelo usado")
    created_at: datetime = Field(default_factory=get_vzla_datetime, sa_type=DateTime(timezone=True))
    description: str = Field(nullable=True, description="Descripción del historial médico")
    patient_id: str = Field(
        foreign_key="patient.id",
        description="Identificador del paciente al que pertenece el historial médico",
    )
    patient: Optional["Patient"] = Relationship(back_populates="medical_histories")
