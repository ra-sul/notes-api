from fastapi import Request, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.users import User
from app.repositories.users import UserRepository
from app.services.users import UserService
from app.dependencies.db import get_db


def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_user_service(repo: UserRepository = Depends(get_user_repo)) -> UserService:
    return UserService(repo)