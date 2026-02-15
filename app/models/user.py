from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from uuid import uuid4

if TYPE_CHECKING:
    from app.models.patient import Patient


class User(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    is_admin: bool = Field(default=False)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    full_name: Optional[str]
    email: str = Field(index=True, unique=True)
    is_active: bool = Field(default=True)
    patients: List["Patient"] = Relationship(back_populates="doctor")
