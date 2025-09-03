import logging

from sqlmodel import Session

from src.core.db import engine, init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    with Session(engine) as session:
        init_db(session)


def main() -> None:
    logger.info("Loading initial data into DB.")
    init()
    logger.info("Initial data loaded.")


if __name__ == "__main__":
    main()
