import logging
import requests
from typing import List, Dict

from kfs.clients.exceptions import APIClientException
from kfs.settings import settings
from kfs.tests.events import events


class APIClient:
    """Client to fetch flight events from the external API."""

    API_URL = settings.API_URL

    def fetch_flight_events(self) -> List[Dict]:
        """Fetches flight events from the external API."""
        try:
            response = requests.get(self.API_URL, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Error fetching events from API: {str(e)}")
            raise APIClientException()


class FakeClient:
    """
    Client to fetch flight events from a predefined list of events for
    testing purposes.
    """

    def fetch_flight_events(self) -> List[Dict]:
        """Returns the list of flight events from the imported events."""
        return events
