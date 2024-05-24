import contextlib
from typing import AsyncIterator, Optional

from loguru import logger
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class PostgresSingleton:
    _engine: Optional[AsyncEngine] = None
    _sessionmaker: Optional[async_sessionmaker] = None

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(PostgresSingleton, cls).__new__(cls)
        return cls.instance

    def init(self, host: str):
        self._engine = create_async_engine(host, pool_pre_ping=True)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self):
        if self._engine is None:
            logger.error("Database Sessionmanager is not initialised")
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            logger.error("Database Sessionmanager is not initialised")
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except:
                await connection.rollback()

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            logger.error("Database Sessionmanager is not initialised")
            raise Exception("DatabaseSessionManager is not initialized")

        sess = self._sessionmaker()
        try:
            yield sess
        except Exception:
            await sess.rollback()
            raise Exception
        finally:
            await sess.close()
