from pydantic import BaseModel, ConfigDict
from typing import Optional

class NoteBase(BaseModel):
    title: str
    body: str

class NotePatch(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None

class NoteCreate(NoteBase):
    pass

class NoteInDB(NoteBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class NoteResponse(NoteInDB):
    pass

