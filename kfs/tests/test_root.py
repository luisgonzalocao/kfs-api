from fastapi.testclient import TestClient

from kfs.main import app
from kfs.settings import settings

client = TestClient(app)


def test_root_endpoint():
    """Test that the root endpoint returns correct metadata."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to KFS API",
        "version": app.version,
        "docs": f"{settings.BASE_URL}/docs",
        "openapi": f"{settings.BASE_URL}/openapi.json",
    }
