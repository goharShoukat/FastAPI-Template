from contextlib import asynccontextmanager

from core.config import settings
from core.database import sessionmanager
from fastapi import FastAPI
from loguru import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Instantiating Postgres")
    sess = sessionmanager()
    sess.init(settings.POSTGRES_URL)
    logger.info("Connection to Postgres established")

    yield
    if sess._engine is not None:
        logger.info("Closing connection to Postgres")
        await sess.close()
        logger.info("Connection to Postgres closed")
