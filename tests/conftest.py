import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.app.models.base import Base
from src.app.models.users import User
from src.app.models.notes import Note
from src.app.repositories.notes import NoteRepository
from src.app.repositories.users import UserRepository


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
def notes_repo(db_session):
    return NoteRepository(db_session)

@pytest.fixture
def users_repo(db_session):
    return UserRepository(db_session)

@pytest.fixture
def user(db_session):
    user = User(name="Admin", password="1234")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def note(db_session, user):
    note = Note(title="Test title", body="Test body", user_id=user.id)
    db_session.add(note)
    db_session.commit()
    db_session.refresh(note)
    return note