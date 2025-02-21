from datetime import datetime, timedelta
from typing import List, Dict
from itertools import combinations

from fastapi import HTTPException

from kfs.clients.client_factory import ClientFactory
from kfs.clients.exceptions import APIClientException
from kfs.utils import parse_datetime
from kfs.settings import settings


class FlightEvent:
    """Represents a single flight event in a journey."""

    def __init__(self, flight_number: str, origin: str, destination: str, departure_time: datetime, arrival_time: datetime):
        self.flight_number = flight_number
        self.origin = origin
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time

    @classmethod
    def from_raw(cls, raw_flight: Dict):
        """Creates a FlightSegment instance from raw API data."""
        return cls(
            flight_number=raw_flight["flight_number"],
            origin=raw_flight["departure_city"],
            destination=raw_flight["arrival_city"],
            departure_time=parse_datetime(raw_flight["departure_datetime"]),
            arrival_time=parse_datetime(raw_flight["arrival_datetime"]),
        )

    def to_dict(self):
        """Formats the flight segment as required by the response."""
        return {
            "flight_number": self.flight_number,
            "from": self.origin,
            "to": self.destination,
            "departure_time": self.departure_time.strftime("%Y-%m-%d %H:%M"),
            "arrival_time": self.arrival_time.strftime("%Y-%m-%d %H:%M"),
        }


class Journey:
    """Represents a full journey, which can include one or multiple flight events."""

    def __init__(self, connections: int, events: List[FlightEvent]):
        self.connections = connections
        self.path = events

    def to_dict(self):
        """Converts journey into API response format."""
        return {
            "connections": self.connections,
            "path": [event.to_dict() for event in self.path],
        }


class SearchService:
    """Handles the flight search logic, finding direct and connecting journeys."""

    def __init__(self, date_str: str, origin: str, destination: str):
        self.date = datetime.strptime(date_str, "%Y-%m-%d").date()
        self.origin = origin
        self.destination = destination

        # Fetch flight events
        try:
            self.client = ClientFactory.get_client()
            self.events = [FlightEvent.from_raw(flight) for flight in self.client.fetch_flight_events()]
        except APIClientException:
            raise HTTPException(
                status_code=503,
                detail="Error fetching flight events from the external API."
            )

        # Find all valid journeys
        self.journeys = self._find_all_journeys()

    def _find_all_journeys(self) -> List[Journey]:
        """Finds all valid journeys"""
        journeys = []

        # Find direct flights
        direct_flights = [
            event for event in self.events
            if event.origin == self.origin
            and event.destination == self.destination
            and event.departure_time.date() == self.date
        ]
        for flight in direct_flights:
            journeys.append(Journey(connections=0, events=[flight]))

        # Find connecting flights
        for num_connections in range(1, settings.MAX_CONNECTIONS + 1):
            # Generate all possible combinations of flights with the given number of connections
            for flight_combination in combinations(self.events, num_connections + 1):
                # Check if the combination forms a valid journey
                if self._is_valid_journey(flight_combination):
                    journeys.append(Journey(connections=num_connections, events=list(flight_combination)))

        return journeys

    def _is_valid_journey(self, flight_combination: List[FlightEvent]) -> bool:
        """Checks if a combination of flights forms a valid journey."""
        # Check if the first flight departs on the search date
        if flight_combination[0].departure_time.date() != self.date:
            return False

        # Check if the journey starts at the origin and ends at the destination
        if flight_combination[0].origin != self.origin or flight_combination[-1].destination != self.destination:
            return False

        # Check if the flights are connected in the correct order
        for i in range(len(flight_combination) - 1):
            if flight_combination[i].destination != flight_combination[i + 1].origin:
                return False

        # Check if the connection time between flights is within the limit
        for i in range(len(flight_combination) - 1):
            connection_time = flight_combination[i + 1].departure_time - flight_combination[i].arrival_time
            if connection_time.total_seconds() > settings.MAX_CONNECTION_TIME_HOURS * 3600:
                return False

        # Check if the total journey time is within 24 hours
        total_journey_time = flight_combination[-1].arrival_time - flight_combination[0].departure_time
        if total_journey_time.total_seconds() > 24 * 3600:
            return False

        return True

    def get_response(self):
        """Returns journeys formatted for API response."""
        return [journey.to_dict() for journey in self.journeys]