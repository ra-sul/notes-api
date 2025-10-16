from sqlalchemy import Column, String, Integer, ForeignKey
from src.app.models.base import Base

class Note(Base):
	__tablename__ = "notes"
	id = Column(Integer, primary_key=True, index=True)
	title = Column(String, index=True)
	body = Column(String)
	user_id = Column(Integer, ForeignKey("users.id"))
