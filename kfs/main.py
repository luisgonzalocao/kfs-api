from fastapi import FastAPI, Query
from datetime import datetime, timedelta
from typing import List, Dict
from kfs.clients.flight_api import FlightAPIClient

app = FastAPI(title="K Flight Searchs", description="API for searching flights", version="1.0.0")

# Initialize the Flight API client
flight_client = FlightAPIClient()


def parse_datetime(datetime_str: str) -> datetime:
    """Parses an ISO 8601 datetime string to a datetime object."""
    return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")


def find_possible_journeys(flight_events: List[Dict], origin: str, destination: str, date: str):
    """Finds possible journeys based on given constraints."""
    date = datetime.strptime(date, "%Y-%m-%d")
    direct_flights = []
    connecting_flights = []

    for flight in flight_events:
        dep_time = parse_datetime(flight["departure_datetime"])
        arr_time = parse_datetime(flight["arrival_datetime"])

        if dep_time.date() != date.date():
            continue  # Only consider flights departing on the given date

        if flight["departure_city"] == origin and flight["arrival_city"] == destination:
            direct_flights.append({"connections": 0, "path": [flight]})

    # Find connections with a maximum of 2 flights
    for flight1 in flight_events:
        if flight1["departure_city"] != origin:
            continue

        for flight2 in flight_events:
            if (
                flight1["arrival_city"] == flight2["departure_city"]
                and flight2["arrival_city"] == destination
            ):
                dep_time1 = parse_datetime(flight1["departure_datetime"])
                arr_time1 = parse_datetime(flight1["arrival_datetime"])
                dep_time2 = parse_datetime(flight2["departure_datetime"])
                arr_time2 = parse_datetime(flight2["arrival_datetime"])

                total_duration = arr_time2 - dep_time1
                connection_time = dep_time2 - arr_time1

                if total_duration <= timedelta(hours=24) and timedelta(hours=0) <= connection_time <= timedelta(hours=4):
                    connecting_flights.append({"connections": 1, "path": [flight1, flight2]})

    return direct_flights + connecting_flights


@app.get("/journeys/search")
def search_journeys(
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
    origin: str = Query(..., min_length=3, max_length=3, description="3-letter origin airport code"),
    destination: str = Query(..., min_length=3, max_length=3, description="3-letter destination airport code"),
):
    """Searches for available journeys based on date, origin, and destination."""
    flight_events = flight_client.fetch_flight_events()
    journeys = find_possible_journeys(flight_events, origin, destination, date)
    return journeys
