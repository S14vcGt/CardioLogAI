from typing import Optional
from pydantic import BaseModel

class UserAuth(BaseModel):
    password: str
    username: str 