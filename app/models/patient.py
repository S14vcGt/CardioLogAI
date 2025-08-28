from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.medical_history import MedicalHistory
    from app.models.user import User

class Patient(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    name: str
    lastname: str
    birth_date: str
    address:str
    cedula: int
    phone: str
    email:str
    doctor_id: str = Field(foreign_key="user.id")
    doctor: Optional["User"] = Relationship(back_populates="patients")
    medical_histories: List["MedicalHistory"] = Relationship(back_populates="patient") 