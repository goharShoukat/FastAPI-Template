from unittest import mock

import pytest
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine

host = "abc"


@pytest.fixture
def singleton():
    from core.database import PostgresSingleton

    return PostgresSingleton()


def test_postgres_singleton_one_instance_only(singleton):
    from core.database import PostgresSingleton

    B = PostgresSingleton()

    assert singleton == B


@mock.patch("core.database.postgres.async_sessionmaker")
@mock.patch("core.database.postgres.create_async_engine")
def test_postgres_init(mock_create_engine, mock_create_session, singleton):
    mock_engine = mock_create_engine.return_value

    singleton.init(host)

    mock_create_engine.assert_called_once_with(host, pool_pre_ping=True)
    mock_create_session.assert_called_once_with(autocommit=False, bind=mock_engine)


@pytest.mark.asyncio
@mock.patch("core.database.postgres.async_sessionmaker")
@mock.patch("core.database.postgres.create_async_engine")
async def test_close(mock_create_engine, mock_create_session, singleton):
    mock_engine = mock.MagicMock(spec=AsyncEngine)

    singleton.init(host)
    singleton._engine = mock_engine

    await singleton.close()

    mock_engine.dispose.assert_called_once()

    assert singleton._engine is None
    assert singleton._sessionmaker is None


@pytest.mark.asyncio
@mock.patch("core.database.postgres.async_sessionmaker")
@mock.patch("core.database.postgres.create_async_engine")
async def test_connect(mock_create_engine, mock_create_session, singleton):
    singleton.init(host)
    mock_engine = mock.MagicMock(spec=AsyncEngine)
    singleton._engine = mock_engine
    mock_connection = mock.AsyncMock()
    mock_engine.begin.return_value.__aenter__.return_value = mock_connection

    async with singleton.connect() as connection:
        assert connection == mock_connection

    mock_engine.begin.assert_called_once()


@pytest.mark.asyncio
@mock.patch("core.database.postgres.async_sessionmaker")
@mock.patch("core.database.postgres.create_async_engine")
async def test_connect_error(mock_create_engine, mock_create_session, singleton):
    singleton.init(host)
    mock_engine = mock.MagicMock(spec=AsyncEngine)
    singleton._engine = mock_engine

    mock_connection = mock.AsyncMock(spec=AsyncConnection)
    mock_engine.begin.return_value.__aenter__.return_value = mock_connection

    mock_engine.begin.side_effect = Exception("Connection failed")

    with pytest.raises(Exception):
        async with singleton.connect():
            pass

    mock_engine.begin.assert_called_once()


@pytest.mark.asyncio
@mock.patch("core.database.postgres.create_async_engine")
async def test_session(mock_create_engine, singleton):
    singleton.init(host)

    async with singleton.session() as session:
        assert session is not None
