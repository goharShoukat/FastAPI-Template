from unittest import mock

import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session


@pytest.mark.asyncio
@mock.patch("api.routes.health_check_.core.initialise_postgres_session")
async def test_healthcheck(mock_postgres):
    from main import app

    mock_postgres.return_value = mock.AsyncMock(spec=Session)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/cero-risks-api")
    assert response.status_code == 200
    assert response.text == '"Healthy Services"'
    mock_postgres.assert_called_once()


@pytest.mark.asyncio
@mock.patch("api.routes.health_check_.core.initialise_postgres_session")
async def test_error_postgres(mock_postgres):
    from main import app

    mock_postgres.side_effect = Exception
    with pytest.raises(Exception):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/cero-risks-api")
