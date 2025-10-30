from src.app.exceptions.base import NotFoundError


class NoteNotFoundError(NotFoundError):
    message = "Note not found"
