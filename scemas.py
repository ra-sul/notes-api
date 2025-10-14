from pydantic import BaseModel, ConfigDict

class NoteBase(BaseModel):
    title: str
    body: str

class Note(NoteBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
