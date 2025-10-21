from sqlalchemy.orm import Session
from src.app.models.notes import Note
from src.app.repositories import notes as notes_repo
from src.app.schemas.notes import NotePatch
from typing import List

def create_note(db: Session, user_id: int, title: str, body: str) -> Note:
	return notes_repo.create_note(db, user_id, title, body)

def get_note(db: Session, user_id: int, note_id: int) -> Note:
	return notes_repo.get_note(db, user_id, note_id)

def update_note(db: Session, user_id: int, note_id: int, new_title: str, new_body: str) -> Note:
	note = get_note(db, user_id, note_id)
	return notes_repo.update_note(db, note, new_title, new_body)

def delete_note(db: Session, user_id: int, note_id: int) -> None:
	note = get_note(db, user_id, note_id)
	notes_repo.delete_note(db, note)

def list_notes(db: Session, user_id: int) -> List[Note]:
	return notes_repo.list_notes(db, user_id)

def patch_note(db: Session, user_id: int, note_id: int, update_data: NotePatch) -> Note:
	note = get_note(db, user_id, note_id)
	return notes_repo.patch_note(db, note, update_data)