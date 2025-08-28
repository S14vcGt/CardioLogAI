from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.patient import Patient

class User(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    full_name: Optional[str]
    email: str = Field(index=True, unique=True)
    is_active: bool = Field(default=True)
    patients: List["Patient"] = Relationship(back_populates="doctor") 