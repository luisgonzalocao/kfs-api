from datetime import timedelta
from typing import List
from itertools import combinations

from kfs.settings import settings
from kfs.services.search_service import Journey, FlightEvent

from abc import ABC


class BaseStrategy(ABC):

    def __init__(self, origin: str, destination: str, events: List[FlightEvent], date):
        self.origin = origin
        self.destination = destination
        self.events = events
        self.date = date

    def fin_all_journeys(self) -> List[Journey]:
        raise NotImplementedError


class IterativeSearchStrategy(BaseStrategy):
    """Handles the flight search logic, finding direct and connecting journeys."""

    def find_all_journeys(self) -> List[Journey]:
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
            journeys.append(Journey(connections=0, path=[flight]))

        # Find connecting flights
        for num_connections in range(1, settings.MAX_CONNECTIONS + 1):
            # Generate all possible combinations of flights with the given number of connections
            for flight_combination in combinations(self.events, num_connections + 1):
                # Check if the combination forms a valid journey
                if self._is_valid_journey(flight_combination):
                    journeys.append(Journey(connections=num_connections, path=list(flight_combination)))

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


class DFSSearchStrategy(BaseStrategy):
    """
    Service that handles the flight search logic, finding direct
    and connecting journeys.

    Implements a Depth-First Search (DFS) to find all possible paths.
    """

    def find_all_journeys(self) -> List[Journey]:
        """Finds all valid journeys from the origin to the destination."""
        journeys = []
        self._dfs(self.origin, [], journeys)
        return journeys

    def _dfs(self,
             current_city: str,
             current_path: List[FlightEvent],
             journeys: List[Journey]):
        """
        Implements a Depth-First Search (DFS) to find all possible paths.

        Args:
            current_city (str): Current city in the search.
            current_path (List[FlightEvent]): Current path of flights.
            journeys (List[Journey]): List of valid journeys found.
        """
        if current_city == self.destination:
            if self._is_valid_journey(current_path):
                journeys.append(Journey(connections=len(current_path) - 1,
                                        path=current_path.copy()))
            return

        for event in self.events:
            if event.origin == current_city:
                if not current_path:
                    if event.departure_time.date() == self.date:
                        current_path.append(event)
                        self._dfs(event.destination, current_path, journeys)
                        current_path.pop()
                else:
                    last_event = current_path[-1]
                    if event.departure_time > last_event.arrival_time and \
                       (event.departure_time - last_event.arrival_time) <= timedelta(hours=settings.MAX_CONNECTION_TIME_HOURS):
                        current_path.append(event)
                        self._dfs(event.destination, current_path, journeys)
                        current_path.pop()

    def _is_valid_journey(self, path: List[FlightEvent]) -> bool:
        """Checks if a journey meets the total duration and maximum
        connections constraints."""
        if not path:
            return False

        total_duration = path[-1].arrival_time - path[0].departure_time
        if total_duration > timedelta(hours=24):
            return False

        if len(path) - 1 > settings.MAX_CONNECTIONS:
            return False

        return True
