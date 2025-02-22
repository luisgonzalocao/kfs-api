from fastapi.testclient import TestClient
from unittest.mock import patch

from kfs.clients.exceptions import APIClientException
from kfs.main import app
from kfs.settings import settings
from kfs.tests.test_services import TEST_EXPECTED_RESPONSE

client = TestClient(app)


def test_search_journeys_503_error():
    """Tests that the API returns a 503 error when the API client fails to fetch flight events."""

    with patch("kfs.clients.factory.ClientFactory.get_client") as mocked:
        return_value = APIClientException("Failed to fetch data")
        mocked.return_value.fetch_flight_events.side_effect = return_value

        response = client.get(settings.SEARCH_URL_PATH,
                              params={"date": "2025-02-21",
                                      "from": "BUE",
                                      "to": "MAD"})

        assert response.status_code == 503
        assert response.json() == {
            "detail": "Error fetching flight events from the external API."
        }


def test_search_journeys(monkeypatch):
    """Tests that the API returns a success responses with status 200"""

    monkeypatch.setattr(settings, "CLIENT_MODE", "TEST")
    response = client.get(settings.SEARCH_URL_PATH,
                          params={"date": "2025-03-10",
                                  "from": "BUE",
                                  "to": "MAD"})
    assert response.status_code == 200
    assert response.json() == TEST_EXPECTED_RESPONSE
