from unittest import mock

import pytest


@mock.patch("core.database.initialise_postgres.PostgresSingleton")
def test_sessionmanager(mock_sing):
    from core.database import sessionmanager

    mock_instance = mock_sing.return_value
    res = sessionmanager()
    mock_sing.assert_called_once()
    assert res == mock_instance


@pytest.mark.asyncio
async def test_initialise_postgres_session():
    from core.database import initialise_postgres_session

    session_manager_mock = mock.MagicMock()
    session_mock = mock.AsyncMock()
    session_manager_mock.session.return_value.__aenter__.return_value = session_mock

    with mock.patch(
        "core.database.initialise_postgres.sessionmanager",
        return_value=session_manager_mock,
    ):
        async for session in initialise_postgres_session():
            assert session == session_mock
