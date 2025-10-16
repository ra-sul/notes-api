from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from src.app.dependencies.db import get_db
from src.app.schemas.users import Login
from src.app.services import users

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(request: Request, login: Login, db: Session = Depends(get_db)):
    current_user = users.login_user(db=db, name=login.name, password=login.password)
    request.session["user_id"] = current_user.id

    return {"message": f"Привет, {current_user.name}!"}

@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return {"message": "Logget out successfully"}