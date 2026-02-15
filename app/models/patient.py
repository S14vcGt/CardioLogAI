from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from uuid import uuid4

if TYPE_CHECKING:
    from app.models.medical_history import MedicalHistory
    from app.models.user import User


class Patient(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    name: str
    lastname: str
    birth_date: str
    address: Optional[str]
    cedula: int = Field(index=True, unique=True)
    phone: Optional[str]
    email: Optional[str] = Field(unique=True)
    sex: str
    family_history: bool
    doctor_id: str = Field(foreign_key="user.id")
    doctor: Optional["User"] = Relationship(back_populates="patients")
    medical_histories: List["MedicalHistory"] = Relationship(back_populates="patient")
