from app.models.users import User
from sqlalchemy.orm import Session

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
            
    def create(self, user) -> User:
        self.db.add(user)
        return user

    def get(self, name: str, password: str) -> User:
        return self.db.query(User).filter(User.name == name, User.password == password).first()

    def get_by_name(self, name: str) -> User:
        return self.db.query(User).filter(User.name == name).first()