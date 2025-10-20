from pydantic import BaseModel, ConfigDict
from typing import Optional

class NoteBase(BaseModel):
    title: str
    body: str

class Note(NoteBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class NoteCreate(NoteBase):
    pass

class NotePatch(NoteBase):
    title: Optional[str] = None
    body: Optional[str] = None