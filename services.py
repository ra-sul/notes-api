from sqlalchemy.orm import Session
import repositories

def register_user(db: Session, name: str, password: str):
	return repositories.create_user(db=db, name=name, password=password)

def login_user(db: Session, name: str, password: str):
	user = repositories.get_user(db=db, name=name, password=password)
	if not user:
		raise ValueError("Пользователь или пароль введены неверно!")
	return user

def add_note_for_user(db: Session, title: str, body: str, user_id: int):
	return repositories.create_note(db=db, title=title, body=body, user_id=user_id)

def select_note(db: Session, note_id: int, user_id: int):
	return repositories.get_note_by_id(db=db, id=note_id, user_id=user_id)

def update_user_note(db: Session, note, new_title: str, new_body: str):
	return repositories.update_note(db=db, note=note, new_title=new_title, new_body=new_body)

def delete_user_note(db: Session, note):
	return repositories.delete_note(db=db, note=note)

def lits_user_notes(db: Session, user_id: int):
	return repositories.get_notes_by_user(db=db, user_id=user_id)