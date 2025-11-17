import pytest
from unittest.mock import Mock

from src.app.services.notes import NoteService
from src.app.models.notes import Note
from src.app.schemas.notes import NoteUpdate, NotePatch
from src.app.exceptions.notes import NoteNotFoundError, NoteAccessDeniedError

@pytest.fixture
def mock_repo():
    repo = Mock()
    return repo


@pytest.fixture
def service(mock_repo):
    return NoteService(mock_repo)


def test_create(service, mock_repo):
    result = service.create(user_id=1, title="Test title", body="Test body")

    assert isinstance(result, Note)
    assert result.user_id == 1
    assert result.title == "Test title"
    assert result.body == "Test body"

    mock_repo.create.assert_called_once_with(result)
    mock_repo.db.commit.assert_called_once()
    mock_repo.db.refresh.assert_called_once_with(result)



def test_get_success(service, mock_repo):
    note = Note(id=1, title="Test title", body="Test body", user_id=1)
    mock_repo.get.return_value = note

    result = service.get(user_id=1, note_id=1)

    assert result is note
    mock_repo.get.assert_called_once_with(1)


def test_get_not_found(service, mock_repo):
    mock_repo.get.return_value = None

    with pytest.raises(NoteNotFoundError):
        service.get(user_id=1, note_id=1)
    
    mock_repo.get.assert_called_once_with(1)


def test_get_access_denied(service, mock_repo):
    mock_repo.get.return_value = Note(id=1, title="Test title", body="Test body", user_id=1)

    with pytest.raises(NoteAccessDeniedError):
        service.get(user_id=999, note_id=1)
    
    mock_repo.get.assert_called_once_with(1)


def test_list(service, mock_repo):
    lst = [Note(id=1, title="Test title", body="Test body", user_id=1)]
    mock_repo.list.return_value = lst

    result = service.list(user_id=1)

    assert result == lst
    mock_repo.list.assert_called_once_with(1)


def test_update(service, mock_repo):
    note = Note(id=1, title="Test title", body="Test body", user_id=1)
    mock_repo.get.return_value = note
    mock_repo.update.return_value = note
    update_data = NoteUpdate(title="Test title", body="Test body")
    data = update_data.model_dump()

    result = service.update(user_id=1, note_id=1, update_data=update_data)

    assert isinstance(result, Note)
    assert result.user_id == 1
    assert result.title == "Test title"
    assert result.body == "Test body"

    mock_repo.update.assert_called_once_with(note, data)
    mock_repo.get.assert_called_once_with(1)
    mock_repo.db.commit.assert_called_once()
    mock_repo.db.refresh.assert_called_once_with(result)


def test_patch(service, mock_repo):
    note = Note(id=1, title="Test title", body="Test body", user_id=1)
    mock_repo.get.return_value = note
    mock_repo.update.return_value = note
    update_data = NotePatch(title="Test title")
    data = update_data.model_dump(exclude_unset=True)

    result = service.patch(user_id=1, note_id=1, update_data=update_data)

    assert isinstance(result, Note)
    assert result.user_id == 1
    assert result.title == "Test title"
    assert result.body == "Test body"

    mock_repo.update.assert_called_once_with(note, data)
    mock_repo.get.assert_called_once_with(1)
    mock_repo.db.commit.assert_called_once()
    mock_repo.db.refresh.assert_called_once_with(result)


def test_delete(service, mock_repo):
    note = Note(id=1, title="Test title", body="Test body", user_id=1)
    mock_repo.get.return_value = note

    service.delete(user_id=1, note_id=1)

    mock_repo.delete.assert_called_once_with(note)
    mock_repo.get.assert_called_once_with(1)
    mock_repo.db.commit.assert_called_once()
