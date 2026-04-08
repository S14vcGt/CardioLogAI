from typing import Optional
from pydantic import BaseModel, ConfigDict


class MedicationEntryCreate(BaseModel):
    """Datos que llegan del frontend para cada medicamento en una historia médica."""
    name: str
    rxcui: Optional[str] = None
    dose: Optional[str] = None
    unit: Optional[str] = None
    frequency: Optional[str] = None


class MedicationEntryRead(BaseModel):
    """Datos de un medicamento asociado a una historia médica (lectura)."""
    id: str  # id del medicamento
    name: str
    rxcui: Optional[str] = None
    dose: Optional[str] = None
    unit: Optional[str] = None
    frequency: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
