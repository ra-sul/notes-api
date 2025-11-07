import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.app.models.base import Base
from src.app.models.notes import Note
from src.app.repositories.notes import NoteRepository

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def repo(db_session):
    return NoteRepository(db=db_session)

@pytest.fixture
def sample_note(db_session):
    note = Note(title="sample_title", body="sample_body", user_id=1)
    db_session.add(note)
    db_session.commit()
    return note
    