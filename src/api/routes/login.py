from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

from src import crud
from src.api.deps import DbSession, CurrentUser
from src.core import authorization
from src.core.config import settings
from src.models import Token

router = APIRouter(tags=["login"])


@router.post("/login/access-token")
def login_access_token(
        session: DbSession, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = crud.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(access_token=authorization.create_access_token(user.id, expires_delta=access_token_expires))


@router.post("/login/test-token")
def test_token(current_user: CurrentUser) -> Any:
    """
    Test access token
    """
    return current_user
