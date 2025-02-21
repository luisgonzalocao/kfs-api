from typing import List, Dict


class BaseClient:
    """Abstract Base Client to fetch flight events."""

    def fetch_flight_events(self) -> List[Dict]:
        """Fetch flight events. Must be implemented by subclasses."""
        raise NotImplementedError("fetch_events() must be implemented by subclasses.")
