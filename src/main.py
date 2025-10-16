from fastapi  import  FastAPI
from contextlib import asynccontextmanager
from starlette.middleware.sessions import SessionMiddleware

from src.app.routes import auth, notes
from src.app.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(notes.router)
app.add_middleware(SessionMiddleware, secret_key="very_secret_key")