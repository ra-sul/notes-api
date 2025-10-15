from sqlalchemy.orm import Session
from src.app.repositories import notes

def add_note_for_user(db: Session, title: str, body: str, user_id: int):
	return notes.create_note(db=db, title=title, body=body, user_id=user_id)

def select_note(db: Session, note_id: int, user_id: int):
	return notes.get_note_by_id(db=db, id=note_id, user_id=user_id)

def update_user_note(db: Session, note, new_title: str, new_body: str):
	return notes.update_note(db=db, note=note, new_title=new_title, new_body=new_body)

def delete_user_note(db: Session, note):
	return notes.delete_note(db=db, note=note)

def list_user_notes(db: Session, user_id: int):
	return notes.get_notes_by_user(db=db, user_id=user_id)