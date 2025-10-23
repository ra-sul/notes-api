from fastapi import APIRouter, Request, Depends, status
from sqlalchemy.orm import Session

from src.app.dependencies.db import get_db
from src.app.schemas.users import UserLogin, UserResponse
from src.app.services import users

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=UserResponse)
def login(request: Request, login: UserLogin, db: Session = Depends(get_db)):
    current_user = users.login_user(db=db, name=login.name, password=login.password)
    request.session["user_id"] = current_user.id

    return {
        "id": current_user.id,
        "name": current_user.name,
        "message": f"Добро пожаловать, {current_user.name}!"
    }

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(request: Request):
    request.session.clear()