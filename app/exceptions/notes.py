from app.exceptions.base import NotFoundError, ForbiddenError


class NoteNotFoundError(NotFoundError):
    message = "Note not found"


class NoteAccessDeniedError(ForbiddenError):
    message = "You do not have permission to access this note"