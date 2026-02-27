import contextlib
from typing import AsyncIterator, Optional

from google.cloud.sql.connector import Connector
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from ..config import settings

Base = declarative_base()


class PostgresSingleton:
    _instance: Optional["PostgresSingleton"] = None
    _engine: Optional[AsyncEngine] = None
    _sessionmaker: Optional[async_sessionmaker] = None
    _connector: Optional[Connector] = None
    _initialised: Optional[bool] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._engine = None
            cls._instance._sessionmaker = None
            cls._instance._initialised = False
            cls._instance._connector = Connector()
        return cls._instance

    def _getconn(self):
        return self._connector.connect_async(
            settings.INSTANCE_CONNECTION_SOCKET,
            "asyncpg",
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            db=settings.DB_NAME,
        )

    async def init(self):
        if self._initialised:
            return

        self._engine = create_async_engine(
            "postgresql+asyncpg://",
            async_creator=self._getconn,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
        )
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)
        self._initialised = True

    async def close(self):
        if self._engine is None:
            raise Exception("Database Sessionmanager is not initialized")
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None
        await self._connector.close_async()

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("Database Connection Manager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception as e:
                await connection.rollback()
                raise e

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("Database Sessionmanager is not initialised")

        sess = self._sessionmaker()
        try:
            yield sess
            await sess.commit()
        except Exception as e:
            await sess.rollback()
            raise e
        finally:
            await sess.close()


pg_sessionmanager = PostgresSingleton()
