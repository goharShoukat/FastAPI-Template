from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from loguru import logger


@pytest.mark.asyncio
@patch("core.lifespan_.pg_sessionmanager")
async def test_lifespan(mock_sess, test_app):
    from core.lifespan_ import lifespan

    mock_sess.init = AsyncMock()
    mock_sess.close = AsyncMock()

    mock_sess.connect.return_value.__aenter__ = AsyncMock()
    mock_sess.connect.return_value.__aexit__ = AsyncMock()

    async with lifespan(test_app):
        pass

    mock_sess.init.assert_awaited_once()
    mock_sess.close.assert_awaited_once()


@pytest.mark.asyncio
@patch("core.lifespan_.pg_sessionmanager")
async def test_lifespan_exception_handling(mock_sess, test_app, caplog):
    from core.lifespan_ import lifespan

    mock_sess.init = AsyncMock()
    mock_sess.close = AsyncMock()
    mock_sess._engine = MagicMock()

    error_msg = "DB Connection Refused"
    mock_sess.connect.return_value.__aenter__.side_effect = Exception(error_msg)

    with pytest.raises(Exception, match=error_msg):
        async with lifespan(test_app):
            pass

    assert "Failed to connect to Postgres" in caplog.text
    assert error_msg in caplog.text
