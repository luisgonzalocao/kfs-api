from unittest import TestCase
from unittest.mock import patch

from kfs.services import SearchService
from kfs.settings import settings


class SearchServiceTestCase(TestCase):

    @patch.object(settings, "CLIENT_MODE", "TEST")
    def test_search_service_with_test_mode_dfs_strategy(self):
        """Tests that SearchService works correctly in TEST mode with
        FakeClient and dfs strategy."""

        search_service = SearchService(date_str="2025-03-10",
                                       origin="BUE",
                                       destination="MAD")

        result = search_service.get_response()
        self.assertEqual(result, TEST_EXPECTED_RESPONSE)

    @patch.object(settings, "CLIENT_MODE", "TEST")
    @patch.object(settings, "MAX_DFS_STRATEGY", 0)
    def test_search_service_with_test_mode_iterative_strategy(self):
        """Tests that SearchService works correctly in TEST mode with
        FakeClient and iterative strategy"""

        search_service = SearchService(date_str="2025-03-10",
                                       origin="BUE",
                                       destination="MAD")

        result = search_service.get_response()
        self.assertEqual(result, TEST_EXPECTED_RESPONSE)


#  For this params = {"date": "2025-03-10", "from": "BUE", "to": "MAD"})
#  This is a expected body response
TEST_EXPECTED_RESPONSE = [
    {
        "connections": 0,
        "path": [
            {
                "flight_number": "XX1001",
                "from": "BUE",
                "to": "MAD",
                "departure_time": "2025-03-10 12:00",
                "arrival_time": "2025-03-10 23:00"
            }
        ]
    },
    {
        "connections": 1,
        "path": [
            {
                "flight_number": "XX1003",
                "from": "BUE",
                "to": "NYC",
                "departure_time": "2025-03-10 14:00",
                "arrival_time": "2025-03-11 04:00"
            },
            {
                "flight_number": "XX1004",
                "from": "NYC",
                "to": "MAD",
                "departure_time": "2025-03-11 06:00",
                "arrival_time": "2025-03-11 09:00"
            }
        ]
    }
]
