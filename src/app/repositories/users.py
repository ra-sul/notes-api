from src.app.models.models import User
from sqlalchemy.orm import Session

def create_user(db: Session, name: str, password: str) -> User:
	new_user = User(name=name, password=password)
	db.add(new_user)
	db.commit()
	db.refresh(new_user)
	return new_user

def get_user(db: Session, name: str, password: str) -> User:
	return db.query(User).filter(User.name == name, User.password == password).first()