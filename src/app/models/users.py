from sqlalchemy import Column, String, Integer, ForeignKey
from src.app.models.base import Base

class User(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True, index=True)
	name = Column(String)
	password = Column(String)