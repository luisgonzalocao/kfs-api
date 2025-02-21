from typing import List, Dict
from .base_client import BaseClient
from kfs.tests.events import events


class FakeClient(BaseClient):
    """
    Client to fetch flight events from a predefined list of events for
    testing purposes.
    """

    def fetch_flight_events(self) -> List[Dict]:
        """Returns the list of flight events from the imported events."""
        return events
