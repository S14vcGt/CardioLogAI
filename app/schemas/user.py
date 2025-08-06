from typing import Optional
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    full_name: Optional[str] = None
    email: str

class UserRead(BaseModel):
    id: int
    username: str
    full_name: Optional[str]
    email: str
    is_active: bool
    class Config:
        orm_mode = True 