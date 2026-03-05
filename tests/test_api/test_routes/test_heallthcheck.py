from unittest import mock

import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

# @pytest.mark.asyncio
# async def test_healthcheck():
#     from main import app

#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         response = await ac.get("/ada")
#     assert response.status_code == 200
#     assert response.text == '"Healthy Services"'
