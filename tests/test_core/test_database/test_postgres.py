from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from core.database.postgres import PostgresSingleton


@pytest.mark.asyncio
async def test_singleton_identity():
    """Verify that multiple calls to constructor return the same instance."""
    db1 = PostgresSingleton()
    db2 = PostgresSingleton()
    assert db1 is db2


@pytest.mark.asyncio
async def test_init_creates_resources():
    """Verify that init sets up the engine and sessionmaker."""
    db = PostgresSingleton()

    # We patch create_async_engine to avoid actual DB connections
    with patch("core.database.postgres.create_async_engine") as mock_create:
        mock_engine = MagicMock()
        mock_create.return_value = mock_engine

        await db.init()

        assert db._initialised is True
        assert db._engine is not None
        assert db._sessionmaker is not None
        mock_create.assert_called_once()


@pytest.mark.asyncio
async def test_close_clears_state():
    """Verify that close disposes the engine and resets attributes."""
    db = PostgresSingleton()
    mock_engine = AsyncMock()
    db._engine = mock_engine
    db._sessionmaker = MagicMock()

    await db.close()

    mock_engine.dispose.assert_awaited_once()
    assert db._engine is None
    assert db._sessionmaker is None


@pytest.mark.asyncio
async def test_connect_context_manager():
    """Verify the connect context manager yields a connection and commits/rolls back."""
    db = PostgresSingleton()
    mock_engine = MagicMock()
    mock_conn = AsyncMock()

    # Setup mock for: async with self._engine.begin() as connection
    mock_engine.begin.return_value.__aenter__.return_value = mock_conn
    db._engine = mock_engine

    async with db.connect() as conn:
        assert conn is mock_conn

    mock_engine.begin.assert_called_once()


@pytest.mark.asyncio
async def test_session_context_manager_success():
    """Verify session commits on success."""
    db = PostgresSingleton()
    mock_sess = AsyncMock()
    mock_maker = MagicMock(return_value=mock_sess)
    db._sessionmaker = mock_maker

    async with db.session() as sess:
        assert sess is mock_sess

    mock_sess.commit.assert_awaited_once()
    mock_sess.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_session_context_manager_rollback():
    """Verify session rolls back on exception."""
    db = PostgresSingleton()
    mock_sess = AsyncMock()
    mock_maker = MagicMock(return_value=mock_sess)
    db._sessionmaker = mock_maker

    with pytest.raises(ValueError):
        async with db.session() as sess:
            raise ValueError("Trigger Rollback")

    mock_sess.rollback.assert_awaited_once()
    mock_sess.close.assert_awaited_once()
