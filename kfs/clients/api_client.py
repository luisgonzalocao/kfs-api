
import os
import requests
from typing import List, Dict
from .base_client import BaseClient
from kfs.settings import settings


class APIClient(BaseClient):
    """Client to fetch flight events from the external API."""

    API_URL = settings.API_URL

    def fetch_flight_events(self) -> List[Dict]:
        """Fetches flight events from the external API."""
        try:
            response = requests.get(self.API_URL, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching events from API: {e}")
            return []
