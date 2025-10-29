from src.app.exceptions.base import NotFoundError, ValidationError


class NoteNotFoundError(NotFoundError):
    message = "Note not found"


class EmptyNoteTitleError(ValidationError):
    message = "Note title cannot be empty"