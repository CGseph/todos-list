from sqlmodel import Session

from src import crud
from src.models import Task, TaskCreate
from tests.utils.user import create_random_user
from tests.utils.utils import random_lower_string


def create_random_task(db: Session) -> Task:
    user = create_random_user(db)
    user_id = user.id
    assert user_id is not None
    title = random_lower_string()
    description = random_lower_string()
    item_in = TaskCreate(title=title, description=description)
    return crud.insert_task(session=db, task_in=item_in, user_id=user_id)
