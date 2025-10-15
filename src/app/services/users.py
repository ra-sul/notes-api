from sqlalchemy.orm import Session
from src.app.repositories import users

def register_user(db: Session, name: str, password: str):
	return users.create_user(db=db, name=name, password=password)

def login_user(db: Session, name: str, password: str):
	user = users.get_user(db=db, name=name, password=password)
	if not user:
		raise ValueError("Пользователь или пароль введены неверно!")
	return user