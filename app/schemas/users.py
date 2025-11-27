from pydantic import BaseModel, ConfigDict, model_validator
from typing import Optional


class UserBase(BaseModel):
    name: str


class UserLogin(UserBase):
    password: str


class UserRegister(UserLogin):
    confirm_password: str
    
    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


class UserOut(UserBase):
    id: int


class UserResponse(UserOut):
    message: Optional[str] = None