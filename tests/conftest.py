import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from unittest.mock import Mock

from app.main import app
from app.models.base import Base
from app.models.users import User
from app.models.notes import Note
from app.repositories.notes import NoteRepository
from app.repositories.users import UserRepository
from app.dependencies.users import get_current_user, get_user_service
from app.dependencies.notes import get_note_service
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
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
def mock_user_service():
	return Mock()

@pytest.fixture
def mock_note_service():
	return Mock()

@pytest.fixture
def mock_current_user():
    return User(id=1, name="Admin", password="1234")

@pytest.fixture
def client(mock_note_service, mock_user_service, mock_current_user):
    app.dependency_overrides = {
        get_note_service: lambda: mock_note_service,
        get_user_service: lambda: mock_user_service,
        get_current_user: lambda: mock_current_user
    }

    with TestClient(app) as c:
        yield c
    
    app.dependency_overrides.clear()


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