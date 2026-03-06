from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.mark.asyncio
@patch("core.lifespan_.pg_sessionmanager")
async def test_lifespan(mock_sess, test_app):
    from core.lifespan_ import lifespan

    # 1. Manually set methods to AsyncMock to allow 'await'
    mock_sess.init = AsyncMock()
    mock_sess.close = AsyncMock()

    # 2. Mock the 'async with connect()' context manager
    # This prevents the "TypeError: 'AsyncMock' object does not support the context manager protocol"
    mock_sess.connect.return_value.__aenter__ = AsyncMock()
    mock_sess.connect.return_value.__aexit__ = AsyncMock()

    async with lifespan(test_app):
        pass

    mock_sess.init.assert_awaited_once()
    mock_sess.close.assert_awaited_once()
