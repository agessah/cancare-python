import secrets

from datetime import datetime, timedelta, UTC
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.events import current_user_id
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.db.models.user import User, Role, ROLE_PERMISSIONS
from app.db.session import get_db

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def generate_token():
    return secrets.token_urlsafe(32)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_token(user_id: int, type: str) -> str:
    expire = datetime.now(UTC) + timedelta(hours=settings.ACTIVATION_TOKEN_EXPIRE_HOURS)

    payload = {
        "sub": str(user_id),
        "type": type,
        "exp": expire
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = decode_token(token)
        user_id = int(payload.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")

    current_user_id.set(user.id)

    return user


def require_role(*roles):
    async def checker(user = Depends(get_current_user)):
        names = {r.name for r in user.roles}

        if not any(role in names for role in roles):
            raise HTTPException(403, "Forbidden")

        return user
    return checker


def require_permission(permission: str):
    async def checker(user = Depends(get_current_user)):
        perms = {
            p.name
            for role in user.roles
            for p in role.permissions
        }

        if permission not in perms:
            raise HTTPException(403, "Forbidden")

        return user
    return checker


def generate_otp():
    return f"{secrets.randbelow(1000000):06}"