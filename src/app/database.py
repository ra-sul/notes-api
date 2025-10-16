from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.models.base import Base

engine = create_engine("sqlite:///./data/test.db")

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():
	Base.metadata.create_all(engine)