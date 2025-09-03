import uuid
from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from enum import Enum
from typing import List


# region User Models

class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class User(UserBase, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.now)

    tasks: List["Task"] = Relationship(back_populates="user")


class UserRead(UserBase):
    id: uuid.UUID


class UsersList(SQLModel):
    users: List[UserRead]
    count: int

# endregion


# region Auth Token
class Token(SQLModel):
    access_token: str
    access_type: str = "bearer"


class JWT(SQLModel):
    sub: str | None = None


# endregion

# region TODOS
class TaskStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"


class TaskBase(SQLModel):
    title: str = Field(max_length=200, index=True)
    description: str = Field(default=None, max_length=500)
    status: TaskStatus = Field(default=TaskStatus.PENDING)


class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, unique=True, index=True, primary_key=True)
    date_created: datetime = Field(default_factory=datetime.now)

    # Foreign keys
    user_id: uuid.UUID = Field(foreign_key="users.id")

    # Relationships
    user: User = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: uuid.UUID
    date_created: datetime
    user_id: int


class TaskUpdate(TaskBase):
    pass

# endregion
