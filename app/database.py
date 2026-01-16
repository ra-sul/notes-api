import os
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from sqlalchemy.exc import OperationalError
from app.core.config import settings
from app.logging_config import logger

engine = create_engine(settings.DATABASE_URL)

for attempt in range(5):
	try:
		with engine.connect() as conn:
			logger.info("Connected to Database!")
			break
	except OperationalError:
		logger.warning(f"Database not ready yet, attempt {attempt}/10. Retrying in 2s...")
		time.sleep(2)
else:
	logger.error("Could not connect to Database after 10 attempts")
	raise Exception("Database connection failed")


SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# def init_db():
# 	Base.metadata.create_all(engine)
