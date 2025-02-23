from unittest import TestCase
from unittest.mock import patch

from datetime import datetime

from kfs.services.strategies import IterativeSearchStrategy, DFSSearchStrategy
from kfs.services.strategy_factory import StrategyFactory
from kfs.services.search_service import FlightEvent
from kfs.settings import settings

events = [
    FlightEvent(
        flight_number="XXX001",
        origin="BUE",
        destination="MAD",
        departure_time=datetime.now(),
        arrival_time=datetime.now(),
    )
]


class SearchStrategiesTestCase(TestCase):

    @patch.object(settings, "MAX_DFS_STRATEGY", 0)
    def test_get_iterative_strategy(self):
        """Tests that the StrategyFactory returns IterativeSearchStrategy when
        settings.MAX_DFS_STRATEGY < len(events)"""

        strategy_class = StrategyFactory.get_strategy_class(events)
        self.assertIs(strategy_class, IterativeSearchStrategy)

    @patch.object(settings, "MAX_DFS_STRATEGY", 1)
    def test_get_dfs_strategy(self):
        """Tests that the StrategyFactory returns DFSSearchStrategy when
        settings.MAX_DFS_STRATEGY >= len(events)"""

        strategy_class = StrategyFactory.get_strategy_class(events)
        self.assertIs(strategy_class, DFSSearchStrategy)
