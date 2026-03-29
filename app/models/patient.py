from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from uuid import uuid4
from sqlalchemy import DateTime
from app.Scripts.general_helpers import get_vzla_datetime
from datetime import datetime
from app.core.const import Sex

if TYPE_CHECKING:
    from app.models.medical_history import MedicalHistory
    from app.models.user import User


class Patient(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    name: str = Field(description="Nombre del paciente")
    lastname: str = Field(description="Apellido del paciente")
    birth_date: str = Field(description="Fecha de nacimiento del paciente")
    address: Optional[str] = Field(default=None, nullable=True, description="Dirección del paciente")
    cedula: int = Field(index=True, unique=True, description="Cédula del paciente")
    phone: Optional[str] = Field(default=None, nullable=True, description="Número de teléfono del paciente")
    email: Optional[str] = Field(default=None, unique=True, nullable=True, description="Correo electrónico del paciente")   
    sex: Sex = Field(description="Sexo del paciente")
    family_history: bool = Field(description="Si el paciente tiene antecedentes familiares de enfermedades cardiacas")
    personal_history: bool = Field(description="Si el paciente tiene antecedentes personales de enfermedades cardiacas")
    created_at: datetime = Field(default_factory=get_vzla_datetime, sa_type=DateTime(timezone=True))
    doctor_id: str = Field(foreign_key="users.id")
    doctor: Optional["User"] = Relationship(back_populates="patients")
    medical_histories: List["MedicalHistory"] = Relationship(back_populates="patient")
