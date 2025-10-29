from src.app.models.users import User
from sqlalchemy.orm import Session

def create_user(db: Session, name: str, password: str) -> User:
	new_user = User(name=name, password=password)
	db.add(new_user)
	return new_user

def get_user(db: Session, name: str, password: str) -> User:
	return db.query(User).filter(User.name == name, User.password == password).first()

def get_user_by_name(db: Session, name: str) -> User:
	return db.query(User).filter(User.name == name).first()