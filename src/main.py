from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from starlette.middleware.sessions import SessionMiddleware

from src.app.routes import auth, notes
from src.app.database import init_db
from src.app.exceptions.base import AppError

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(notes.router)
app.add_middleware(SessionMiddleware, secret_key="very_secret_key")

@app.exception_handler(AppError)
async def app_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.__class__.__name__, "detail": exc.message}
    )