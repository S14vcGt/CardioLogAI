from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class MedicalHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    date: datetime = Field(default_factory=datetime.utcnow)
    description: str
    patient: Optional["Patient"] = Relationship(back_populates="medical_histories") 