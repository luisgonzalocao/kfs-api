from typing import Union

from kfs.settings import settings
from kfs.clients.clients import APIClient, FakeClient


class ClientFactory:
    """Factory class to create the appropriate client based on settings."""

    @classmethod
    def get_client(cls) -> Union[APIClient, FakeClient]:
        """Returns an instance of the appropriate client."""
        return {"TEST": FakeClient, "API": APIClient}[settings.CLIENT_MODE]()
