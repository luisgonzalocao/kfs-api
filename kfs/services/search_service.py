import logging
from datetime import datetime
from typing import List, Dict
from fastapi import HTTPException

from kfs.clients.client_factory import ClientFactory
from kfs.clients.exceptions import APIClientException
from kfs.services.strategy_factory import StrategyFactory


class FlightEvent:
    """
    Represents a single flight event.

    Attributes:
        flight_number (str): Flight number.
        origin (str): Code of the origin city.
        destination (str): Code of the destination city.
        departure_time (datetime): Departure date and time.
        arrival_time (datetime): Arrival date and time.
    """

    def __init__(self,
                 flight_number: str,
                 origin: str, destination: str,
                 departure_time: datetime,
                 arrival_time: datetime):
        self.flight_number = flight_number
        self.origin = origin
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time

    @classmethod
    def from_raw(cls, raw_flight: Dict) -> 'FlightEvent':
        """Creates a FlightEvent instance from a raw flight dictionary."""
        return cls(
            flight_number=raw_flight["flight_number"],
            origin=raw_flight["departure_city"],
            destination=raw_flight["arrival_city"],
            departure_time=datetime.fromisoformat(raw_flight["departure_datetime"]),
            arrival_time=datetime.fromisoformat(raw_flight["arrival_datetime"]),
        )

    def to_dict(self) -> Dict:
        """Converts the FlightEvent instance to a dictionary."""
        return {
            "flight_number": self.flight_number,
            "from": self.origin,
            "to": self.destination,
            "departure_time": self.departure_time.strftime("%Y-%m-%d %H:%M"),
            "arrival_time": self.arrival_time.strftime("%Y-%m-%d %H:%M"),
        }


class Journey:
    """
    Represents a complete journey, which can include one or multiple flight events.

    Attributes:
        connections (int): Number of connections in the journey.
        path (List[FlightEvent]): List of flights that make up the journey.
    """

    def __init__(self, connections: int, path: List[FlightEvent]):
        self.connections = connections
        self.path = path

    def to_dict(self) -> Dict:
        """
        Converts the Journey instance to a dictionary.

        Returns:
            Dict: Dictionary containing journey information.
        """
        return {
            "connections": self.connections,
            "path": [event.to_dict() for event in self.path],
        }


class SearchService:
    """
    Service that handles the flight search logic, finding direct
    and connecting journeys.

    Attributes:
        date (date): Search date.
        origin (str): Code of the origin city.
        destination (str): Code of the destination city.
        events (List[FlightEvent]): List of available flight events.
        journeys (List[Journey]): List of valid journeys found.
    """

    def __init__(self, date_str: str, origin: str, destination: str):
        self.date = datetime.strptime(date_str, "%Y-%m-%d").date()
        self.origin = origin
        self.destination = destination

        self.client = ClientFactory.get_client()
        self.events = self._fetch_events()

        self.strategy_class = StrategyFactory.get_strategy_class(self.events)
        self.strategy = self.strategy_class(origin=self.origin,
                                            destination=self.destination,
                                            events=self.events,
                                            date=self.date)
        # Find all valid journeys
        self.journeys = self.strategy.find_all_journeys()

    def _fetch_events(self):
        try:
            return [FlightEvent.from_raw(flight) for flight in self.client.fetch_flight_events()]
        except APIClientException:
            detail = "Error fetching flight events from the external API."
        except Exception as e:
            logging.error(f"Unexpected Exception:  {str(e)}")
            detail = "Unexpected error fetching flight events."
        raise HTTPException(
            status_code=503,
            detail=detail)

    def get_response(self) -> List[Dict]:
        """Returns the found journeys in the format required by the API."""
        return [journey.to_dict() for journey in self.journeys]
