import pytest
from unittest.mock import Mock

from src.app.services.users import UserService
from src.app.models.users import User
from src.app.exceptions.users import UserAlreadyExistsError, InvalidCredentialsError

@pytest.fixture
def mock_repo():
    repo = Mock()
    return repo


@pytest.fixture
def service(mock_repo):
    return UserService(mock_repo)


def test_register_success(service, mock_repo):
    mock_repo.get_by_name.return_value = None
    
    result = service.register(name="Admin", password="1234")

    assert result.name == "Admin"
    assert result.password == "1234"

    mock_repo.get_by_name.assert_called_once_with("Admin")
    mock_repo.create.assert_called_once_with(result)
    mock_repo.db.commit.assert_called_once()
    mock_repo.db.refresh.assert_called_once_with(result)


def test_register_user_already_exists(service, mock_repo):
    mock_repo.get_by_name.return_value = User(name="Admin", password="1234")

    with pytest.raises(UserAlreadyExistsError):
        service.register(name="Admin", password="1234")
    
    mock_repo.get_by_name.assert_called_once_with("Admin")


def test_login_success(service, mock_repo):
    mock_repo.get.return_value = User(name="Admin", password="1234")

    result = service.login(name="Admin", password="1234")
    
    assert result.name == "Admin"
    assert result.password == "1234"

    mock_repo.get.assert_called_once_with("Admin", "1234")


def test_login_invalid_credentials(service, mock_repo):
    mock_repo.get.return_value = None

    with pytest.raises(InvalidCredentialsError):
        service.login(name="Admin", password="1234")
    
    mock_repo.get.assert_called_once_with("Admin", "1234") 