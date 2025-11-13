from datetime import timedelta, datetime, timezone
from fastapi import HTTPException, APIRouter, Depends
from pydantic import BaseModel
from starlette import status
from typing import Annotated
from .database import db_dependency
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.models import User
from dotenv import load_dotenv
import jwt
import os


load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET") or "SEC_REC_PY"
ALGORITHM = os.getenv("ALGORITHM") or "HS256"
JWT_EXPIRES_IN = os.getenv("JWT_EXPIRES_IN") or "7d"


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenRefreshRequest(BaseModel):
    refresh_token: str


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/token")


def parse_duration(duration: str) -> timedelta:
    """
    Convert duration strings like '7d', '60m', '12h', '30s' into timedelta.
    """
    unit = duration[-1]
    value = int(duration[:-1])
    
    if unit == "d":
        return timedelta(days=value)
    elif unit == "h":
        return timedelta(hours=value)
    elif unit == "m":
        return timedelta(minutes=value)
    elif unit == "s":
        return timedelta(seconds=value)
    else:
        raise ValueError(f"Unsupported duration unit: {unit}")


def authenticate_user(email: str, password: str, db):
    user = db.query(User).filter(User.email == email).first()
    if not user or not bcrypt_context.verify(password, user.password):
        return False

    return user


def create_access_token(user: dict, expires_delta: timedelta = parse_duration(JWT_EXPIRES_IN)):
    if expires_delta:
        expires = datetime.now(timezone.utc) + expires_delta
    else:
        expires = datetime.now(timezone.utc) + timedelta(minutes=60)
    encoded_info = {"username": user["sub"], "exp": expires}

    return jwt.encode(encoded_info, SECRET_KEY, algorithm=ALGORITHM)


async def authenticate(
    token: Annotated[str, Depends(oauth2_bearer)], db: db_dependency
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username: str = payload.get("username")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user!"
            )

        user = db.query(User).filter(User.username == username).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found!"
            )

        return {"id": user.id, "username": user.username, "email": user.email}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current token has expired!",
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token!",
        )

auth_dependency = Annotated[dict, Depends(authenticate)]
