from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from typing import Optional, Any

SECRET_KEY = "VERY_SECRET_KEY_1234"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

def create_acces_token(data: dict, expire_delta: Optional[timedelta] = None) -> str:
	to_encode = data.copy()
	if expire_delta:
		expire = datetime.now(timezone.utc) + expire_delta
	else:
		expire = datetime.now(timezone.utc) + timedelta(15)
	
	to_encode.update({"exp": expire})
	
	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt

def verify_token(token: str) -> dict[str, Any]:
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
		return payload
	except JWTError:
		return None