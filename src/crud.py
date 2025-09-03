import uuid
from fastapi import HTTPException
from typing import Any, List
from alembic.util import status
from pydantic import EmailStr
from sqlmodel import Session, select
from src.core.authorization import get_password_hash, verify_password
from src.models import User, UserCreate, Task, TasksList, TaskRead, TaskCreate


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_user_by_email(*, session: Session, email: EmailStr) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: EmailStr, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


# region Tasks crud

def get_tasks(*, session: Session, offset: int, limit: int) -> Any:
    query = select(Task).offset(offset).limit(limit)
    return session.exec(query).all()


def get_user_tasks(session: Session,
                   user_id: uuid.UUID, offset: int, limit: int) -> Any:
    query = (
        select(Task)
        .where(Task.user_id == user_id)
        .offset(offset)
        .limit(limit)
    )
    return session.exec(query).all()


def get_task_by_id(session: Session, task_id: uuid.UUID) -> Task | None:
    task = session.get(Task, task_id)
    if not task:
        return None
    return task


def insert_task(session: Session, task_in: TaskCreate, user_id: uuid.UUID) -> Task:
    task = Task.model_validate(task_in, update={"user_id": user_id})
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def update_task(session: Session, task: Task, task_dict: dict) -> Task:
    task.sqlmodel_update(task_dict)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task(session: Session, task: Task) -> bool:
    session.delete(task)
    session.commit()
    return True

# end region
