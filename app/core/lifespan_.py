from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from sqlalchemy import text


from .database.postgres import pg_sessionmanager


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Instantiating Postgres")
    pg_sessionmanager
    await pg_sessionmanager.init()
    try:
        async with pg_sessionmanager.connect() as connection:
            result = await connection.execute(text("SELECT 1"))
            test_result = result.scalar()
            if test_result == 1:
                logger.info("Connection to Postgres established and verified")
            else:
                logger.error("Connection test returned unexpected result")
                raise Exception("Database connection test failed")
    except Exception as e:
        logger.error(f"Failed to connect to Postgres: {str(e)}")
        if pg_sessionmanager._engine is not None:
            await pg_sessionmanager.close()
        raise e

    yield

    if pg_sessionmanager._engine is not None:
        logger.info("Closing connection to Postgres")
        await pg_sessionmanager.close()
        logger.info("Connection to Postgres closed")
