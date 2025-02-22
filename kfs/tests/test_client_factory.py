from kfs.clients.clients import APIClient, FakeClient
from kfs.clients.factory import ClientFactory
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
