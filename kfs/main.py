import logging

from fastapi import FastAPI, Query, Depends, Request

from kfs.services import SearchService
from kfs.settings import settings
from kfs.utils import validate_date

# Logging global config
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Initialize FastAPI app
app = FastAPI(title=settings.SERVICE_NAME,
              description=settings.SERVICE_DESCRIPTION,
              version=settings.VERSION)


@app.get("/", include_in_schema=False)
def root():
    return {
        "message": settings.SERVICE_NAME,
        "version": settings.VERSION,
        "docs": settings.DOCS_URL,
        "openapi": settings.OPENAPI_URL,
        "settings": {
            "CLIENT_MODE": settings.CLIENT_MODE,
            "MAX_CONNECTIONS": settings.MAX_CONNECTIONS,
            "MAX_JOURNEY_DURATION_HOURS": settings.MAX_JOURNEY_DURATION_HOURS,
            "MAX_CONNECTION_TIME_HOURS":  settings.MAX_CONNECTION_TIME_HOURS
        }
    }


@app.get(settings.SEARCH_PATH)
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
