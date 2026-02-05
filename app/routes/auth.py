from fastapi import APIRouter, Request, Response, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.users import get_user_service
from app.dependencies.refresh_tokens import get_refresh_token_service
from app.schemas.users import UserLogin, UserResponse, UserRegister
from app.schemas.tokens import TokenResponse, RefreshRequest, RefreshLogout
from app.services.users import UserService
from app.logging_config import logger
from app.auth.jwt_utils import create_acces_token, create_refresh_token, verify_token, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from app.services.refresh_tokens import RefreshTokenService
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
def login(
    request: Request, 
    login: UserLogin, 
    user_service: UserService = Depends(get_user_service),
    refresh_token_service: RefreshTokenService = Depends(get_refresh_token_service)
    ):
    user = user_service.login(name=login.name, password=login.password)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_acces_token(
        data={"sub": str(user.id)},
        expire_delta=access_token_expires
    )

    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token, jti = create_refresh_token(
        data={"sub": str(user.id)},
        expire_delta=refresh_token_expires
        )
    
    refresh_token_service.create(user_id=user.id, jti=jti)

    logger.info("User %s logged in", user.id)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh")
def refresh(
    request: RefreshRequest,
    refresh_token_service: RefreshTokenService = Depends(get_refresh_token_service)
    ):
    payload = verify_token(request.refresh_token, token_type="refresh")

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    jti = payload.get("jti")
    user_id = payload.get("sub")

    db_token = refresh_token_service.get(jti)

    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has been revoked or expired"
        )
    
    access_token = create_acces_token({"sub": user_id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    request: RefreshLogout, 
    refresh_token_service: RefreshTokenService = Depends(get_refresh_token_service)
    ):
    payload = verify_token(request.refresh_token, token_type="refresh")
    if payload:
        jti = payload.get("jti")
        refresh_token_service.revoke(jti)