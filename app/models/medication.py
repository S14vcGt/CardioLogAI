from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from uuid import uuid4

if TYPE_CHECKING:
    from app.models.medical_history import MedicalHistory


class MedicalHistoryMedication(SQLModel, table=True):
    """Tabla intermedia muchos-a-muchos entre MedicalHistory y Medication.
    Almacena la dosis, unidad y frecuencia específicas de cada prescripción."""

    __tablename__ = "medicalhistorymedication"

    id: Optional[str] = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
    )
    medical_history_id: str = Field(foreign_key="medicalhistory.id", description="ID de la historia médica")
    medication_id: str = Field(foreign_key="medication.id", description="ID del medicamento")
    dose: Optional[str] = Field(default=None, nullable=True, description="Dosis (ej: 500, 10-20)")
    unit: Optional[str] = Field(default=None, nullable=True, description="Unidad (ej: mg, g, mL)")
    frequency: Optional[str] = Field(default=None, nullable=True, description="Frecuencia (ej: Cada 8 horas)")

    # Relaciones
    medication: Optional["Medication"] = Relationship(back_populates="history_links")
    medical_history: Optional["MedicalHistory"] = Relationship(back_populates="medication_links")


class Medication(SQLModel, table=True):
    """Medicamento. Se reutiliza entre pacientes e historias médicas."""

    id: Optional[str] = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
    )
    name: str = Field(index=True, description="Nombre del medicamento")
    rxcui: Optional[str] = Field(default=None, nullable=True, index=True, description="Código RxCUI de RxNorm")

    # Relación inversa hacia la tabla intermedia
    history_links: List["MedicalHistoryMedication"] = Relationship(back_populates="medication")
