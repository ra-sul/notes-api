from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean
from datetime import datetime, timezone
from app.models.base import Base

class RefreshToken(Base):
	__tablename__ = "refresh_tokens"
	
	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
	jti = Column(String(256), unique=True, nullable=False, index=True)
	expires_at = Column(DateTime, nullable=False)
	is_revoked = Column(Boolean, default=False)
	created_at = Column(DateTime, default= lambda: datetime.now(timezone.utc))