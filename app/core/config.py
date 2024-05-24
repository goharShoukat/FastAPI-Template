import warnings
from typing import Callable, List

from decouple import config
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings

from utils import configure_logging

warnings.simplefilter(action="ignore", category=FutureWarning)


class Settings(BaseSettings):
    HOST: str = config("HOST", cast=str)
    PORT: int = config("PORT", cast=int)
    WORKERS: int = config("WORKERS", cast=int)
    API_V1_STR: str = "/api"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = config("ALLOWED_ORIGINS").split(",")

    PROJECT_NAME: str = "CEROInsightsAPI"

    POSTGRES_URL: str = (
        "postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}".format(
            DB_USER=config("DB_USER", cast=str),
            DB_PASSWORD=config("DB_PASSWORD", cast=str),
            DB_HOST=config("DB_HOST", cast=str),
            DB_NAME=config("DB_NAME", cast=str),
        )
    )

    def logging(self) -> Callable:
        return configure_logging()

    class Config:
        case_sensitive = True


settings = Settings()
