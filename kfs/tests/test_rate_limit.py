import pytest
from fastapi.testclient import TestClient
from kfs.main import app, limiter
from kfs.settings import settings

client = TestClient(app)


@pytest.fixture
def override_rate_limit(monkeypatch):
    """Temporarily override RATE_LIMIT setting and reload limiter."""
    original_rate_limit = settings.RATE_LIMIT

    # Override RATE_LIMIT just for this test
    monkeypatch.setattr(settings, "RATE_LIMIT", "1/minute")

    # Reapply rate limiting only to the correct route
    search_route = next(route for route in app.router.routes if route.path == settings.SEARCH_URL_PATH)
    limiter.limit(settings.RATE_LIMIT)(search_route.endpoint)

    yield  # Run the test

    # Restore original rate limit
    monkeypatch.setattr(settings, "RATE_LIMIT", original_rate_limit)
    limiter.limit(original_rate_limit)(search_route.endpoint)


def test_rate_limit_exceeded(override_rate_limit):
    """Test that the rate limit is enforced correctly."""
    url = "/journeys/search?date=2024-09-12&from=BUE&to=MAD"

    # First request should pass
    response = client.get(url)
    assert response.status_code == 200

    # Second request should be blocked
    response = client.get(url)
    assert response.status_code == 429
