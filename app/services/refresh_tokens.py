from datetime import datetime, timezone, timedelta
from typing import List

from app.repositories.refresh_tokens import RefreshTokenRepository
from app.models.refresh_tokens import RefreshToken
from app.auth.jwt_utils import REFRESH_TOKEN_EXPIRE_DAYS

class RefreshTokenService():
	def __init__(self, repo: RefreshTokenRepository):
		self.repo = repo
	
	def create(self, user_id: int, jti: str):
		expires_at = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
		new_token = RefreshToken(user_id=user_id, jti=jti, expires_at=expires_at)
		self.repo.create(new_token)
		self.repo.db.commit()
		self.repo.db.refresh(new_token)
		return new_token
	
	def get(self, jti: str) -> RefreshToken:
		return self.repo.get(jti=jti)
	
	def revoke(self, jti: str) -> RefreshToken:
		token = self.get(jti=jti)
		revoked_token = self.repo.revoke(token)
		self.repo.db.commit()
		return revoked_token
	
	def revoke_all_by_user(self, user_id: int) -> List[RefreshToken]:
		tokens = self.repo.revoke_all_by_user(user_id=user_id)
		self.repo.db.commit()
		return tokens
	
	def cleanup_expired(self):
		self.repo.cleanup_expired()