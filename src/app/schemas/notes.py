from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class NoteBase(BaseModel):
    title: str
    body: str


class NotePatch(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None


class NoteCreate(NoteBase):
    title: str = Field(min_length=1, max_length=50)


class NoteInDB(NoteBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class NoteResponse(NoteInDB):
    pass

