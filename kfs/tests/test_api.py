from fastapi.testclient import TestClient
from unittest.mock import patch

from kfs.clients.exceptions import APIClientException
from kfs.main import app
from kfs.settings import settings

client = TestClient(app)


def test_search_journeys_503_error():
    """Tests that the API returns a 503 error when the API client fails to fetch flight events."""

    with patch("kfs.clients.client_factory.ClientFactory.get_client") as mock_get_client:
        mock_get_client.return_value.fetch_flight_events.side_effect = APIClientException("Failed to fetch data")

        response = client.get(settings.SEARCH_URL_PATH,
                              params={"date": "2025-02-21", "from": "BUE", "to": "MAD"})

        assert response.status_code == 503
        assert response.json() == {"detail": "Error fetching flight events from the external API."}
