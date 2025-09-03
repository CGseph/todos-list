from fastapi import FastAPI
from src.core.config import settings
from src.api.main import router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_VERSION_STR}/openapi.json",
    version=settings.PROJECT_VERSION,
)


app.include_router(router, prefix=settings.API_VERSION_STR)


if settings.ENVIRONMENT == "dev":
    @app.get("/env", tags=["debug"])
    def read_environment():
        return settings.model_dump()
