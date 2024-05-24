import pytest
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def mock_settings_env_vars(monkeypatch):
    monkeypatch.setenv("HOST", "folder")
    monkeypatch.setenv("PORT", "123")
    monkeypatch.setenv("WORKERS", "1")
    monkeypatch.setenv(
        "ALLOWED_ORIGINS",
        "http://google.com,http://google.com",
    )

    monkeypatch.setenv("DB_USER", "1")
    monkeypatch.setenv("DB_PASSWORD", "1")
    monkeypatch.setenv("DB_HOST", "1")
    monkeypatch.setenv("DB_NAME", "1")


@pytest.fixture
def test_app():
    from main import app

    client = TestClient(app)
    yield client
