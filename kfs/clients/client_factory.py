from .base_client import BaseClient
from kfs.settings import settings
from kfs.clients.api_client import APIClient
from kfs.clients.fake_client import FakeClient

CLIENT_MODE_CLASSES = {
        "TEST": FakeClient,
        "API": APIClient,
    }


class ClientFactory:
    """Factory class to create the appropriate client based on env."""

    @staticmethod
    def get_client() -> BaseClient:
        """Returns an instance of the appropriate client."""
        return CLIENT_MODE_CLASSES[settings.CLIENT_MODE]()
