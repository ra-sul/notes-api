from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.repositories.refresh_tokens import RefreshTokenRepository
from app.services.refresh_tokens import RefreshTokenService

def get_refresh_token_repo(db: Session = Depends(get_db)) -> RefreshTokenRepository:
	return RefreshTokenRepository(db=db)

def get_refresh_token_service(repo: RefreshTokenRepository = Depends(get_refresh_token_repo)):
	return RefreshTokenService(repo=repo)