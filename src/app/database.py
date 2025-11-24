from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.models.base import Base

DATABASE_URL = "postgresql+psycopg2://project_user:qwerty@localhost:5432/myproject"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():
	from src.app.database import DATABASE_URL
	print("FACTUAL DATABASE_URL:", DATABASE_URL)
	Base.metadata.create_all(engine)
