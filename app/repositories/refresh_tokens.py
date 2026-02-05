from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List

from app.models.refresh_tokens import RefreshToken


class RefreshTokenRepository():
	def __init__(self, db: Session):
		self.db = db
	
	def create(self, token: RefreshToken) -> RefreshToken:
		self.db.add(token)
		return token
	
	def get(self, jti: str) -> RefreshToken:
		return self.db.query(RefreshToken).filter(
			RefreshToken.jti == jti, 
			RefreshToken.is_revoked == False,
			RefreshToken.expires_at > datetime.now(timezone.utc)
			).first()
	
	def revoke(self, token: RefreshToken) -> RefreshToken:
		token.is_revoked = True
		return token
	
	def revoke_all_by_user(self, user_id: int) -> List[RefreshToken]:
		tokens = self.db.query(RefreshToken).filter(
			RefreshToken.user_id == user_id,
			RefreshToken.is_revoked == False
		).all()

		for token in tokens:
			token.is_revoked = True
		
		return tokens
	
	def cleanup_expired(self):
		self.db.query(RefreshToken).filter(
			RefreshToken.expires_at < datetime.now(timezone.utc)
		).delete()