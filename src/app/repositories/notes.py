from src.app.models.notes import Note
from src.app.schemas.notes import NotePatch
from sqlalchemy.orm import Session
from typing import List, Optional

def create_note(db: Session, user_id: int, title: str, body: str) -> Note:
    new_note = Note(title=title, body=body, user_id=user_id)
    db.add(new_note)
    return new_note

def get_note(db: Session, user_id: int, note_id: int) -> Optional[Note]:
    return db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()

def list_notes(db: Session, user_id: int) -> List[Note]:
    return db.query(Note).filter(Note.user_id == user_id).all()

def update_note(note: Note, new_title: str, new_body: str) -> Note:
    note.title = new_title
    note.body = new_body
    return note

def patch_note(note: Note, update_data: NotePatch) -> Note:

    update_fields  = update_data.model_dump(exclude_unset=True)

    for key, value in update_fields.items():
        setattr(note, key, value)
    
    return note

def delete_note(db: Session, note: Note) -> None:
    db.delete(note)