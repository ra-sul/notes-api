from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    name: str
    password: str

class Login(UserBase):
    model_config = ConfigDict(from_attributes=True)