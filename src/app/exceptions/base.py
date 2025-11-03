class AppError(Exception):
    message = "An unexpected error occured"
    status_code = 500

    def __init__(self, message: str | None = None):
        if message:
            self.message = message
        super().__init__(self.message)


class NotFoundError(AppError):
    status_code = 404


class UnauthorizedError(AppError):
    status_code = 401


class ConflictError(AppError):
    status_code = 409


class ForbiddenError(AppError):
    status_code = 403
