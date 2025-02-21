import json
from typing import List, Dict
from .base_client import BaseClient


class FakeClient(BaseClient):
    """
    Client to fetch flight events from a local JSON file for
    testing purposes.
    """

    FILE_PATH = "kfs.tests.events.json"

    def fetch_flight_events(self) -> List[Dict]:
        """Loads flight events from a local JSON file."""
        try:
            with open(self.FILE_PATH, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading local flight events: {e}")
            return []
