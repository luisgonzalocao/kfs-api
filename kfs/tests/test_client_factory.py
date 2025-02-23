from unittest import TestCase
from unittest.mock import patch

from kfs.clients import APIClient, FakeClient
from kfs.clients.factory import ClientFactory
from kfs.settings import settings


class ClientFactoryTestCase(TestCase):

    @patch.object(settings, "CLIENT_MODE", "TEST")
    def test_get_client_test_mode(self):
        """Tests that the ClientFactory returns FakeClient when CLIENT_MODE
        is 'TEST'."""

        client = ClientFactory.get_client()
        self.assertIsInstance(client, FakeClient)

    @patch.object(settings, "CLIENT_MODE", "API")
    def test_get_client_api_mode(self):
        """Tests that the ClientFactory returns APIClient when CLIENT_MODE
        is 'API'."""
        client = ClientFactory.get_client()
        self.assertIsInstance(client, APIClient)
