from typing import Optional
from pydantic import BaseModel

class UserCreate(BaseModel):
    password: str
    username: str
    full_name:Optional[str]
    email: str

class UserRead(BaseModel):
    id: str
    username: str
    full_name: Optional[str]
    email: str
    is_active: bool
    class Config:
        from_attributes = True 