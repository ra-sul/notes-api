import pytest
from unittest.mock import Mock

from app.models.users import User
from app.exceptions.users import UserAlreadyExistsError, InvalidCredentialsError


def test_register(client, mock_user_service):
    mock_user_service.register.return_value = User(id=1, name="Admin", password="1234")

    result = client.post("/auth/register", json={"name": "Admin", "password": "1234", "confirm_password": "1234"})

    assert result.status_code == 201
    assert result.json() == {
        "id": 1,
        "name": "Admin",
        "message": "Successful registration!"
    }

    mock_user_service.register.assert_called_once_with(name="Admin", password="1234")


def test_register_user_already_exists(client, mock_user_service):
    mock_user_service.register.side_effect = UserAlreadyExistsError()

    result = client.post("/auth/register", json={"name": "Admin", "password": "1234", "confirm_password": "1234"})

    assert result.status_code == 409
    assert result.json() == {
        "error": "UserAlreadyExistsError",
        "detail": "User with this name already exists"
    }


def test_login(client, mock_user_service, mock_refresh_token_service, mocker):
    mock_user_service.login.return_value = User(id=1, name="Admin", password="1234")
    mocker.patch("app.routes.auth.create_access_token",return_value="access_token_123")
    mocker.patch("app.routes.auth.create_refresh_token", return_value=("refresh_token_123", "jti_123"))

    result = client.post("/auth/login", json={"name": "Admin", "password": "1234"})

    assert result.status_code == 200

    data = result.json()

    assert data["access_token"] == "access_token_123"
    assert data["refresh_token"] == "refresh_token_123"
    assert data["token_type"] == "bearer"

    mock_user_service.login.assert_called_once_with(
        name="Admin",
        password="1234"
    )

    mock_refresh_token_service.create.assert_called_once_with(
        user_id=1,
        jti="jti_123"
    )


def test_login_invalid_credentials(client, mock_user_service):
    mock_user_service.login.side_effect = InvalidCredentialsError()

    result = client.post("/auth/login", json={"name": "Admin", "password": "1234"})

    assert result.status_code == 401
    assert result.json() == {
        "error": "InvalidCredentialsError",
        "detail": "Invalid username or password"
    }


def test_logout(client, mock_refresh_token_service, mocker):
    mocker.patch(
        "app.routes.auth.verify_token",
        return_value={"jti": "jti_123"}
    )

    result = client.post(
        "/auth/logout",
        json={"refresh_token": "refresh_token_123"}
    )

    assert result.status_code == 204

    mock_refresh_token_service.revoke.assert_called_once_with("jti_123")