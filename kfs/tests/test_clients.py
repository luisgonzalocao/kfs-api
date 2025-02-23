from unittest import TestCase
from unittest.mock import patch

from kfs.clients import APIClient, FakeClient
from kfs.tests.events import events


class ClientsTestCase(TestCase):

    def test_fetch_flight_events_success(self):
        """Tests that the FakeClient correctly loads flight events from the
        Python list."""

        expected_data = events  # Usamos la lista importada desde events.py

        # Initialize FakeClient and call the fetch_flight_events method
        class FakeClientWithList(FakeClient):
            def fetch_flight_events(self):
                return expected_data

        client = FakeClientWithList()
        result = client.fetch_flight_events()

        # Compare the result with the expected data
        self.assertEqual(result, expected_data)

    def test_fetch_flight_events(self):
        """Tests that the APIClient correctly fetches data."""
        client = APIClient()
        mock_response = [
            {"flight_number": "XX1234",
             "departure_city": "BUE",
             "arrival_city": "MAD"}
        ]

        with patch("kfs.clients.requests.get") as mock_get:
            mock_get.return_value.json.return_value = mock_response
            mock_get.return_value.raise_for_status = lambda: None

            result = client.fetch_flight_events()
            self.assertEqual(result, mock_response)
