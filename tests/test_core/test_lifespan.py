from unittest import mock

import pytest


@pytest.mark.asyncio
@mock.patch("core.lifespan_.settings")
@mock.patch("core.lifespan_.sessionmanager")
async def test_lifespan(mock_manager, mock_settings, test_app):
    from core import lifespan

    sess = mock_manager.return_value
    sess.init = mock.AsyncMock()
    sess.close = mock.AsyncMock()

    async with lifespan(test_app):
        pass

    mock_manager.assert_called_once()
    sess.init.assert_called_once_with(mock_settings.POSTGRES_URL)
