from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl, computed_field
from pydantic_core import MultiHostUrl


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )

    PROJECT_NAME: str = "TODOs List API"
    PROJECT_VERSION: str = "1.0.0"

    API_VERSION_STR: str = "/api/v1"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 2
    ENVIRONMENT: str = "dev"

    # DATABASE SETTINGS
    DATABASE_URL: AnyUrl
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432
    POSTGRES_SERVER: str

    @computed_field
    @property
    def POSTGRES_DATABASE_URL(self) -> str:
        return str(MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB
        ))


settings = Settings()
