from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime


class PatientCreate(BaseModel):
    name: str
    lastname: str
    birth_date: str
    address: str
    cedula: int
    phone: str
    email: str
    sex: str
    family_history: bool
    doctor_id: Optional[str]

    model_config = ConfigDict(from_attributes=True)

    @field_validator("birth_date")
    @classmethod
    def validar_formato_fecha(cls, v: str) -> str:
        try:
            # Intentamos convertir el texto a fecha real
            # Si la fecha no existe, esto fallará
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError(
                "La fecha de naciemiento debe tener el formato dd-mm-aaaa (ej: 1995-12-23)"
            )


class PatientRead(BaseModel):
    id: int
    name: str
    lastname: str
    birth_date: str
    address: str
    cedula: int
    phone: str
    email: str
    family_history: bool

    model_config = ConfigDict(from_attributes=True)
