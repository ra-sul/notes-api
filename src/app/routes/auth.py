from fastapi import APIRouter, Request, Depends, status
from sqlalchemy.orm import Session

from src.app.dependencies.db import get_db
from src.app.schemas.users import UserLogin, UserResponse, UserRegister
from src.app.services import users

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register(register: UserRegister, db: Session = Depends(get_db)):
    new_user = users.register_user(db=db, name=register.name, password=register.password)
    return {
        "id": new_user.id,
        "name": new_user.name,
        "message": f"Successful registration!"
    }


@router.post("/login", response_model=UserResponse)
def login(request: Request, login: UserLogin, db: Session = Depends(get_db)):
    current_user = users.login_user(db=db, name=login.name, password=login.password)
    request.session["user_id"] = current_user.id
    return {
        "id": current_user.id,
        "name": current_user.name,
        "message": f"Welcome, {current_user.name}!"
    }


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(request: Request):
    request.session.clear()