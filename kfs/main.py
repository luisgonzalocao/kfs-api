import logging
from fastapi import FastAPI, Query, Depends

from kfs.services.search_service import SearchService
from kfs.utils import validate_date

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Kiu Flight Service", description="API for searching flights", version="2.0.0")


@app.get("/journeys/search")
def search_journeys(
    date: str = Depends(validate_date),
    from_: str = Query(..., alias="from", min_length=3, max_length=3,
                       description="origin airport code"),
    to: str = Query(..., min_length=3, max_length=3,
                    description="destination airport code"),
):
    service = SearchService(date_str=date, origin=from_, destination=to)
    return service.journeys
