from sqlmodel import create_engine, SQLModel, Session, select
from sqlalchemy.engine import Engine
from src.core.config import settings
from src.models import User, UserCreate
from src import crud

engine = create_engine(str(settings.POSTGRES_DATABASE_URL))


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_engine() -> Engine:
    return engine


def init_db(session: Session):
    user = session.exec(
        select(User).where(User.email == settings.DEFAULT_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.DEFAULT_SUPERUSER,
            password=settings.DEFAULT_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)
