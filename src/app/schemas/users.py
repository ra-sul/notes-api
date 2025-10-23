from pydantic import BaseModel, ConfigDict
from typing import Optional

class UserBase(BaseModel):
    name: str

class UserLogin(UserBase):
    password: str

class UserOut(UserBase):
    id: int

class UserResponse(UserOut):
    message: Optional[str] = None