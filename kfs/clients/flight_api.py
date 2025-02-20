import requests
from typing import List, Dict


class FlightAPIClient:
    """Client to fetch flight events from an external API."""

    BASE_URL = "https://mock.apidog.com/m1/814105-793312-default/flight-events"

    def fetch_flight_events(self) -> List[Dict]:
        """Fetches flight events from the external API."""
        try:
            response = requests.get(self.BASE_URL, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching flight events: {e}")
            return []
