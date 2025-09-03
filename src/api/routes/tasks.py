import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from src.api.deps import CurrentUser, DbSession
from src.models import Task, TaskCreate, TaskRead, TasksList, TaskUpdate, Message
from src import crud

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=TasksList)
def read_tasks(
        session: DbSession, current_user: CurrentUser, offset: int = 0, limit: int = 100
) -> TasksList:
    """
    Retrieve user tasks.
    """

    if current_user.is_superuser:
        tasks = crud.get_tasks(session=session, offset=offset, limit=limit)
    else:
        tasks = crud.get_user_tasks(session, current_user.id, offset, limit)

    return TasksList(tasks=tasks, count=len(tasks))


@router.get("/{id}", response_model=TaskRead)
def read_task(session: DbSession, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get task by ID.
    """
    task = crud.get_task_by_id(session, id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not current_user.is_superuser and (task.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not your task")
    return task


@router.post("/", response_model=TaskRead)
def create_task(
        *, session: DbSession, current_user: CurrentUser, task_in: TaskCreate
) -> Any:
    """
    Create new task.
    """
    return crud.insert_task(session, task_in, current_user.id)


@router.put("/{id}", response_model=TaskRead)
def update_task(
        *,
        session: DbSession,
        current_user: CurrentUser,
        id: uuid.UUID,
        task_in: TaskUpdate,
) -> Any:
    """
    Update a task.
    """
    task = crud.get_task_by_id(session, id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not current_user.is_superuser and (task.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not your task")
    update_dict = task_in.model_dump(exclude_unset=True)

    return crud.update_task(session, task, update_dict)


@router.delete("/{id}")
def delete_task(
        session: DbSession, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete a task.
    """
    task = crud.get_task_by_id(session, id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not current_user.is_superuser and (task.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not your task")
    crud.delete_task(session, task)

    return Message(message="Task deleted")
