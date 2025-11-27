import pytest
from unittest.mock import Mock

from app.models.notes import Note
from app.models.users import User
from app.exceptions.notes import NoteNotFoundError
from app.schemas.notes import NotePatch


def test_list_notes(client, mock_note_service):
	mock_note_service.list.return_value = [Note(id=1, title="Test title", body="Test body")]

	response = client.get("/notes/")

	assert response.status_code == 200
	assert response.json() == [{"id": 1, "title": "Test title", "body": "Test body"}]

	mock_note_service.list.assert_called_once_with(user_id=1)


def test_get_note(client, mock_note_service):
	mock_note_service.get.return_value = Note(id=1, title="Test title", body="Test body")

	response = client.get("/notes/1")

	assert response.status_code == 200
	assert response.json() == {"id": 1, "title": "Test title", "body": "Test body"}

	mock_note_service.get.assert_called_once_with(user_id=1, note_id=1)


def test_get_note_not_found(client, mock_note_service):
	mock_note_service.get.side_effect = NoteNotFoundError()

	response = client.get("/notes/1")

	assert response.status_code == 404
	assert response.json() == {
		"error": "NoteNotFoundError",
		"detail": "Note not found"
	}


def test_create_note(client, mock_note_service):
	mock_note_service.create.return_value = Note(id=1, title="Test title", body="Test body")

	response = client.post("/notes/", json={"title": "Test title", "body": "Test body"})

	assert response.status_code == 201
	assert response.json() == {"id": 1, "title": "Test title", "body": "Test body"}
	
	mock_note_service.create.assert_called_once_with(user_id=1, title="Test title", body="Test body")


def test_patch_note(client, mock_note_service):
	mock_note_service.patch.return_value = Note(id=1, title="Updated title", body="Test body")
	update_data = {"title": "Updated title"}
	response = client.patch("/notes/1", json=update_data)

	assert response.status_code == 200
	assert response.json() == {"id": 1, "title": "Updated title", "body": "Test body"}
	
	mock_note_service.patch.assert_called_once_with(user_id=1, note_id=1, update_data=NotePatch(**update_data))


def test_delete_note(client, mock_note_service):
	response = client.delete("/notes/1")

	assert response.status_code == 204

	mock_note_service.delete.assert_called_once_with(user_id=1, note_id=1)