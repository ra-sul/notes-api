from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Note(Base):
	__tablename__ = "notes"
	id = Column(Integer, primary_key=True, index=True)
	title = Column(String, index=True)
	body = Column(String)
	user_id = Column(Integer, ForeignKey("users.id"))

class User(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True, index=True)
	name = Column(String)
	password = Column(String)