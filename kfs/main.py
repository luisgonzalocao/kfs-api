import logging

from fastapi import FastAPI, Query, Depends, Request

from kfs.services.search_service import SearchService
from kfs.utils import validate_date
from kfs.settings import settings

# Logging global config
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Initialize FastAPI app
app = FastAPI(title="KFS",
              description="API for searching journeys",
              version="1.0.0")


@app.get("/", include_in_schema=False)
def root():
    return {
        "message": "Welcome to KFS API",
        "version": settings.VERSION,
        "docs": f"{settings.BASE_URL}/docs",
        "openapi": f"{settings.BASE_URL}/openapi.json",
    }


@app.get(settings.SEARCH_URL_PATH)
def search_journeys(
    request: Request,
    date: str = Depends(validate_date),
    from_: str = Query(...,
                       alias="from",
                       min_length=3,
                       max_length=3,
                       description="Origin airport code"),
    to: str = Query(...,
                    min_length=3,
                    max_length=3,
                    description="Destination airport code"),
):
    """Search for available journeys based on date, origin, and destination."""
    return SearchService(date_str=date,
                         origin=from_,
                         destination=to).get_response()
