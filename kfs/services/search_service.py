from datetime import datetime, timedelta
from typing import List, Dict, Set, Tuple
from kfs.clients.client_factory import ClientFactory
from kfs.utils import parse_datetime
from kfs.settings import settings


class FlightSegment:
    """Represents a single flight segment in a journey."""

    def __init__(self, flight_number: str, departure_city: str, arrival_city: str,
                 departure_time: datetime, arrival_time: datetime):
        self.flight_number = flight_number
        self.from_city = departure_city
        self.to_city = arrival_city
        self.departure_time = departure_time
        self.arrival_time = arrival_time

    @classmethod
    def from_raw(cls, raw_flight: Dict):
        """Creates a FlightSegment instance from raw API data."""
        return cls(
            flight_number=raw_flight["flight_number"],
            departure_city=raw_flight["departure_city"],
            arrival_city=raw_flight["arrival_city"],
            departure_time=parse_datetime(raw_flight["departure_datetime"]),
            arrival_time=parse_datetime(raw_flight["arrival_datetime"]),
        )

    def to_dict(self):
        """Formats the flight segment as required by the response."""
        return {
            "flight_number": self.flight_number,
            "from": self.from_city,
            "to": self.to_city,
            "departure_time": self.departure_time.strftime("%Y-%m-%d %H:%M"),
            "arrival_time": self.arrival_time.strftime("%Y-%m-%d %H:%M"),
        }


class Journey:
    """Represents a full journey, which can include one or multiple flight segments."""

    def __init__(self, connections: int, segments: List[FlightSegment]):
        self.connections = connections
        self.path = segments

    def to_dict(self):
        """Converts journey into API response format."""
        return {
            "connections": self.connections,
            "path": [segment.to_dict() for segment in self.path],
        }


class SearchService:
    """Handles the flight search logic, finding direct and connecting journeys."""

    def __init__(self, date_str: str, origin: str, destination: str):
        self.date = datetime.strptime(date_str, "%Y-%m-%d").date()
        self.origin = origin
        self.destination = destination

        # Fetch flight events
        self.client = ClientFactory.get_client()
        self.flight_events = [FlightSegment.from_raw(flight) for flight in self.client.fetch_flight_events()]

        # Find all valid journeys
        self.journeys = self._find_all_journeys()

    def _find_all_journeys(self) -> List[Journey]:
        """Finds all possible journeys (direct and connecting flights) with constraints."""
        seen_routes: Set[Tuple] = set()
        valid_journeys = []

        # Start with flights that depart from the origin
        routes = [[flight] for flight in self.flight_events if flight.from_city == self.origin]

        for _ in range(settings.MAX_CONNECTIONS + 1):  # Allow up to MAX_CONNECTIONS
            new_routes = []
            for route in routes:
                last_flight = route[-1]

                # If this route reaches the destination, add it
                if last_flight.to_city == self.destination:
                    route_key = tuple((seg.flight_number, seg.from_city, seg.to_city) for seg in route)

                    if route_key not in seen_routes:
                        seen_routes.add(route_key)
                        valid_journeys.append(Journey(len(route) - 1, route))

                # Expand with new connections
                new_routes += [
                    route + [next_flight]
                    for next_flight in self.flight_events
                    if (
                        last_flight.to_city == next_flight.from_city  # Must connect
                        and next_flight.to_city != self.origin  # Avoid returning to origin
                        and timedelta(hours=settings.MIN_CONNECTION_TIME_HOURS) 
                           <= (next_flight.departure_time - last_flight.arrival_time) 
                           <= timedelta(hours=settings.MAX_CONNECTION_TIME_HOURS)  # Connection valid
                        and (next_flight.arrival_time - route[0].departure_time) 
                           <= timedelta(hours=settings.MAX_JOURNEY_DURATION_HOURS)  # Full journey valid
                    )
                ]

            routes += new_routes  # Add new routes for next iteration

        return valid_journeys

    def get_response(self):
        """Returns journeys formatted for API response."""
        return [journey.to_dict() for journey in self.journeys]
