from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

engine = create_engine("sqlite:///./test.db")

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():
	Base.metadata.create_all(engine)