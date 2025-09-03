from fastapi import APIRouter
from src.api.routes import utils, users, login, tasks

router = APIRouter()
router.include_router(utils.router)
router.include_router(login.router)
router.include_router(users.router)
router.include_router(tasks.router)
