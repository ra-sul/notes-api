from models import Note, User
from sqlalchemy.orm import Session


def create_user(db: Session, name: str, password: str) -> User:
	new_user = User(name=name, password=password)
	db.add(new_user)
	db.commit()
	db.refresh(new_user)
	return new_user

def get_user(db: Session, name: str, password: str) -> User:
	return db.query(User).filter(User.name == name, User.password == password).first()

def create_note(db: Session, title: str, body: str, user_id: int) -> Note:
	new_note = Note(title=title, body=body, user_id=user_id)
	db.add(new_note)
	db.commit()
	db.refresh(new_note)
	return new_note

def get_note_by_id(db: Session, id: int, user_id: int) -> Note:
	return db.query(Note).filter(Note.id == id, Note.user_id == user_id).first()

def get_notes_by_user(db: Session, user_id: int) -> list[Note]:
	return db.query(Note).filter(Note.user_id ==user_id).all()

def update_note(db: Session, note: Note, new_title: str, new_body: str) -> Note:
	note.title = new_title
	note.body = new_body
	db.commit()
	db.refresh(note)
	return note

def delete_note(db: Session, note: Note):
	db.delete(note)
	db.commit()