from src.app.repositories.users import UserRepository
from src.app.models.users import User
from src.app.exceptions.users import InvalidCredentialsError, UserAlreadyExistsError

class UserService:
	def __init__(self, repo: UserRepository):
		self.repo = repo

	def register(self, name: str, password: str) -> User:
		user = self.repo.get_by_name(name)
		if user:
			raise UserAlreadyExistsError()
		
		new_user = User(name=name, password=password)
		self.repo.create(new_user)
		self.repo.db.commit()
		self.repo.db.refresh(new_user)
		return new_user

	def login(self, name: str, password: str) -> User:
		user = self.repo.get(name, password)
		if not user:
			raise InvalidCredentialsError()
		return user