"""
Minimal API-key based auth for demo purposes.
Swap this for full OAuth2/JWT user flows when you extend the project —
the JWT helpers below are already wired up for that upgrade.
"""
from datetime import datetime, timedelta

from fastapi import Header, HTTPException, status
from jose import jwt, JWTError

from app.config import settings

DEMO_API_KEY = "semantiq-dev-key"


def verify_api_key(x_api_key: str = Header(default="")):
    if x_api_key != DEMO_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
    return True


def create_access_token(subject: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")


def decode_access_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
