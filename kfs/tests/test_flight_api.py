from kfs.clients.api_client import APIClient
from unittest.mock import patch


def test_fetch_flight_events():
    """Tests that the API client correctly fetches data."""
    client = APIClient()
    mock_response = [{"flight_number": "XX1234", "departure_city": "BUE", "arrival_city": "MAD"}]

    with patch("kfs.clients.api_client.requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.raise_for_status = lambda: None

        result = client.fetch_flight_events()
        assert result == mock_response
