from fastapi import APIRouter
from src.api.routes import utils

router = APIRouter()
router.include_router(utils.router)
