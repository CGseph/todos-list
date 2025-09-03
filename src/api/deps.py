from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session
from src.core.config import settings
from src.core.db import engine
from src.models import User, JWT

oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_VERSION_STR}/login/access-token"
)


def get_db():
    with Session(engine) as session:
        yield session


AuthDep = Annotated[str, Depends(oauth2)]
DbSession = Annotated[Session, Depends(get_db)]


def get_current_user(session: DbSession, token: AuthDep) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = JWT(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials.",
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def is_superuser(user: CurrentUser) -> User:
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return User

