from fastapi import APIRouter, Request, Depends, status
from sqlalchemy.orm import Session

from src.app.dependencies.users import get_user_service
from src.app.schemas.users import UserLogin, UserResponse, UserRegister
from src.app.services.users import UserService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register(register: UserRegister, service: UserService = Depends(get_user_service)):
    new_user = service.register(name=register.name, password=register.password)
    return {
        "id": new_user.id,
        "name": new_user.name,
        "message": f"Successful registration!"
    }


@router.post("/login", response_model=UserResponse)
def login(request: Request, login: UserLogin, service: UserService = Depends(get_user_service)):
    current_user = service.login(name=login.name, password=login.password)
    request.session["user_id"] = current_user.id
    return {
        "id": current_user.id,
        "name": current_user.name,
        "message": f"Welcome, {current_user.name}!"
    }


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(request: Request):
    request.session.clear()