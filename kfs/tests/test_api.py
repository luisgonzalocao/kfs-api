from fastapi.testclient import TestClient

from unittest import TestCase
from unittest.mock import patch

from kfs.clients.exceptions import APIClientException
from kfs.main import app
from kfs.settings import settings
from kfs.tests.test_services import TEST_EXPECTED_RESPONSE


class APITestCase(TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.mock_path = "kfs.clients.factory.ClientFactory.get_client"

    def test_search_journeys_503_error(self):
        """Tests that the API returns a 503 error when the API client fails to
        fetch flight events."""

        with patch(self.mock_path) as mocked:
            return_value = APIClientException()
            mocked.return_value.fetch_flight_events.side_effect = return_value

            response = self.client.get(settings.SEARCH_PATH,
                                       params={"date": "2025-02-21",
                                               "from": "BUE",
                                               "to": "MAD"})

            self.assertEqual(response.status_code, 503)
            self.assertEqual(
                response.json(),
                {"detail": "Error fetching flight events from the external API."}
            )

    def test_search_journeys_503_error_unexpected(self):
        """Tests that the API returns a 503 error when catchs a
        Unexpected Exception"""

        with patch(self.mock_path) as mocked:
            return_value = Exception()
            mocked.return_value.fetch_flight_events.side_effect = return_value

            response = self.client.get(settings.SEARCH_PATH,
                                       params={"date": "2025-02-21",
                                               "from": "BUE",
                                               "to": "MAD"})

            self.assertEqual(response.status_code, 503)
            self.assertEqual(
                response.json(),
                {"detail": 'Unexpected error fetching flight events.'}
            )

    @patch.object(settings, "CLIENT_MODE", "TEST")
    def test_search_journeys(self):
        """Tests that the API returns a success responses with status 200"""

        response = self.client.get(settings.SEARCH_PATH,
                                   params={"date": "2025-03-10",
                                           "from": "BUE",
                                           "to": "MAD"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), TEST_EXPECTED_RESPONSE)

    def test_root_endpoint(self):
        """Test that the root endpoint returns correct metadata."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "message": settings.SERVICE_NAME,
                "version": settings.VERSION,
                "docs": settings.DOCS_URL,
                "openapi": settings.OPENAPI_URL,
                "settings": {
                    "CLIENT_MODE": settings.CLIENT_MODE,
                    "MAX_CONNECTIONS": settings.MAX_CONNECTIONS,
                    "MAX_JOURNEY_DURATION_HOURS": settings.MAX_JOURNEY_DURATION_HOURS,
                    "MAX_CONNECTION_TIME_HOURS":  settings.MAX_CONNECTION_TIME_HOURS
                }
            }
        )
