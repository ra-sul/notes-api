from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from typing import Optional, Any
import uuid

from app.core.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS

def create_access_token(data: dict, expire_delta: Optional[timedelta] = None) -> str:
	to_encode = data.copy()
	if expire_delta:
		expire = datetime.now(timezone.utc) + expire_delta
	else:
		expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	
	to_encode.update({"exp": expire, "type": "access"})
	
	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt

def create_refresh_token(data: dict, expire_delta: Optional[timedelta] = None) -> tuple[str, str]:
	to_encode = data.copy()
	if expire_delta:
		expire = datetime.now(timezone.utc) + expire_delta
	else:
		expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
	
	jti = str(uuid.uuid4().hex)

	to_encode.update({
		"exp": expire, 
		"type": "refresh",
		"jti": jti
		})
	
	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt, jti

def verify_token(token: str, token_type: str = "access") -> dict[str, Any]:
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
		
		if payload.get("type") != token_type:
			return None
		
		return payload
	except JWTError:
		return None