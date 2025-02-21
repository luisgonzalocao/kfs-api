from fastapi.testclient import TestClient
from kfs.main import app

client = TestClient(app)


def test_search_journeys():
    """Tests that the API endpoint responds correctly."""
    response = client.get("/journeys/search?date=2024-09-12&from=BUE&to=PMI")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
