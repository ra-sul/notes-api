from app.exceptions.base import UnauthorizedError, ConflictError


class InvalidCredentialsError(UnauthorizedError):
    message = "Invalid username or password"


class UserAlreadyExistsError(ConflictError):
    message = "User with this name already exists"