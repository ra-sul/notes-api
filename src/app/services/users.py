from sqlalchemy.orm import Session
from src.app.repositories import users
from src.app.models.users import User

def register_user(db: Session, name: str, password: str) -> User:
	return users.create_user(db=db, name=name, password=password)

def login_user(db: Session, name: str, password: str) -> User:
	user = users.get_user(db=db, name=name, password=password)
	if not user:
		raise ValueError("Пользователь или пароль введены неверно!")
	return user