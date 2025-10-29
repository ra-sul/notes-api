from sqlalchemy.orm import Session

from src.app.repositories import users as users_repo
from src.app.models.users import User
from src.app.exceptions.users import InvalidCredentialsError, UserAlreadyExistsError

def register_user(db: Session, name: str, password: str) -> User:
	user = users_repo.get_user_by_name(db=db, name=name)

	if user:
		raise UserAlreadyExistsError()

	new_user = users_repo.create_user(db=db, name=name, password=password)
	db.commit()
	db.refresh(new_user)
	return new_user

def login_user(db: Session, name: str, password: str) -> User:
	user = users_repo.get_user(db=db, name=name, password=password)
	if not user:
		raise InvalidCredentialsError()
	return user