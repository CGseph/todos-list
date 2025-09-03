import uuid
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from src.api.deps import is_superuser, DbSession, CurrentUser
from sqlmodel import select
from src.models import User, UsersList, UserRead, UserCreate
from src.core.config import settings
from src import crud

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me",
            response_model=UserRead)
def read_me(current_user: CurrentUser) -> Any:
    """
    Get current user.
    """
    return current_user


# region SuperUser endpoints

@router.get("/",
            dependencies=[Depends(is_superuser)],
            response_model=UsersList)
def query_users(session: DbSession, offset: int = 0, limit: int = 50) -> Any:
    """
    Query all registered users
    """
    state = select(User).offset(offset).limit(limit)
    users = session.exec(state).all()

    return UsersList(users=users, count=len(users))


@router.post("/",
             dependencies=[Depends(is_superuser)],
             response_model=UserRead)
def create_user(*, session: DbSession, user_in: UserCreate) -> Any:
    """
    Create new user.
    """
    user = crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user already exists.",
        )

    user = crud.create_user(session=session, user_create=user_in)
    return user


@router.get("/{id}",
            dependencies=[Depends(is_superuser)],
            response_model=UserRead)
def read_user(*, session: DbSession, id: uuid.UUID):
    """
    Get a user information
    """
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# endregion


