import pytest
from unittest.mock import Mock

from src.app.models.notes import Note
from src.app.models.users import User

@pytest.fixture
def mock_note_service():
	return Mock()

@pytest.fixture
def mock_current_user():
    return User(id=1, name="Admin", password="1234")

def test_list_notes(client, mock_note_service):
	mock_note_service.list.return_value = [Note(id=1, title="Test title", body="Test body")]

	response = client.get("/notes/")

	assert response.status_code == 200
	assert response.json() == [{"id": 1, "title": "Test title", "body": "Test body"}]

	mock_note_service.list.assert_called_once()

