from src.app.models.notes import Note
from src.app.schemas.notes import NotePatch
from sqlalchemy.orm import Session
from typing import List, Optional

class NoteRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, note: Note) -> Note:
        self.db.add(note)
        return note

    def get(self, note_id: int) -> Optional[Note]:
        return self.db.query(Note).filter(Note.id == note_id).first()

    def list(self, user_id: int) -> List[Note]:
        return self.db.query(Note).filter(Note.user_id == user_id).all()

    def update(self, note: Note, data: dict) -> Note:
        for key, value in data.items():
            setattr(note, key, value)
        
        return note

    def delete(self, note: Note) -> None:
        self.db.delete(note)