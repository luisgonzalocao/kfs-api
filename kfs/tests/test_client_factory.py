from kfs.clients.api_client import APIClient
from kfs.clients.fake_client import FakeClient
from kfs.clients.client_factory import ClientFactory
from kfs.settings import settings


def test_get_client_test_mode(monkeypatch):
    """Tests that the ClientFactory returns FakeClient when CLIENT_MODE is 'TEST'."""

    monkeypatch.setattr(settings, "CLIENT_MODE", "TEST")
    client = ClientFactory.get_client()
    assert isinstance(client, FakeClient)


def test_get_client_api_mode(monkeypatch):
    """Tests that the ClientFactory returns APIClient when CLIENT_MODE is 'API'."""

    monkeypatch.setattr(settings, "CLIENT_MODE", "API")
    client = ClientFactory.get_client()
    assert isinstance(client, APIClient)
