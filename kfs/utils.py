import re
from datetime import datetime
from fastapi import HTTPException, Query


def parse_datetime(datetime_str: str) -> datetime:
    """Converts an ISO 8601 datetime string to a datetime object."""
    return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")


def validate_date(
    date: str = Query(..., description="Date in YYYY-MM-DD format")
) -> str:
    """
    Extracts 'date' from query params, shows the description in Swagger,
    and validates the format and real existence of the date.
    """
    DATE_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}$")

    # Validate with regex first
    if not DATE_REGEX.match(date):
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Must be YYYY-MM-DD (e.g., 2025-03-10)."
        )

    # Validate it's a real date
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Non-existent calendar date. (e.g., 2024-02-30 is invalid)."
        )

    return date  # Return the validated date
