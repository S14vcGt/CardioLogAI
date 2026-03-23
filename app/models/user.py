from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from uuid import uuid4
from sqlalchemy import DateTime
from app.Scripts.general_helpers import get_vzla_datetime
from datetime import datetime

if TYPE_CHECKING:
    from app.models.patient import Patient


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    is_admin: bool = Field(default=False, description="Indica si el usuario es administrador")
    username: str = Field(index=True, unique=True, description="Nombre de usuario")
    hashed_password: str = Field(description="Contraseña hasheada")
    full_name: Optional[str] = Field(description="Nombre completo del usuario")
    email: str = Field(index=True, unique=True, description="Correo electrónico del usuario")
    is_active: bool = Field(default=True, description="Indica si el usuario está activo")
    created_at: datetime = Field(default_factory=get_vzla_datetime, sa_type=DateTime(timezone=True))
    patients: List["Patient"] = Relationship(back_populates="doctor")
