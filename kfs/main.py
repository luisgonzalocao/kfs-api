from fastapi import FastAPI, Query, Depends, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from kfs.services.search_service import SearchService
from kfs.utils import validate_date
from kfs.settings import settings

# Initialize FastAPI app
app = FastAPI(title="KFS",
              description="API for searching journeys",
              version="1.0.0")

# Initialize the rate limiter
limiter = Limiter(key_func=get_remote_address, default_limits=[])
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

# Add SlowAPI Middleware
app.add_middleware(SlowAPIMiddleware)


@app.get(settings.SEARCH_URL_PATH)
@limiter.limit(settings.RATE_LIMIT, override_defaults=False)
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
    return SearchService(date_str=date, origin=from_, destination=to).journeys
