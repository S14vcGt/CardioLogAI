from typing import Optional
from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):
    password: str
    username: str
    full_name:Optional[str]
    email: str

    model_config = ConfigDict(from_attributes=True) 

class UserRead(BaseModel):
    id: str
    username: str
    full_name: Optional[str]
    email: str
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True) 

class UserUpdate (BaseModel):
    id: str
    username: str
    full_name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    is_admin: bool

    model_config = ConfigDict(from_attributes=True) 