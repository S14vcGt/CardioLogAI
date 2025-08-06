from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Patient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    birth_date: str
    owner_id: int = Field(foreign_key="user.id")
    owner: Optional["User"] = Relationship(back_populates="patients")
    medical_histories: List["MedicalHistory"] = Relationship(back_populates="patient") 