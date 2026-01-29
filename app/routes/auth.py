from fastapi import APIRouter, Request, Response, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.users import get_user_service
from app.schemas.users import UserLogin, UserResponse, UserRegister
from app.schemas.auth import TokenResponse
from app.services.users import UserService
from app.logging_config import logger
from app.auth.jwt_utils import create_acces_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(register: UserRegister, service: UserService = Depends(get_user_service)):
    new_user = service.register(name=register.name, password=register.password)
    logger.info("User %s registered", new_user.id)
    return {
        "id": new_user.id,
        "name": new_user.name,
        "message": "Successful registration!"
    }


@router.post("/login", response_model=TokenResponse)
def login(request: Request, login: UserLogin, service: UserService = Depends(get_user_service)):
    user = service.login(name=login.name, password=login.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_acces_token(
        data={"sub": str(user.id)},
        expire_delta=access_token_expires
    )

    logger.info("User %s logged in", user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(request: Request, response: Response):
    pass