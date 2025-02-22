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


def test_get_iterative_strategy(monkeypatch):
    """Tests that the StrategyFactory returns IterativeSearchStrategy when
    settings.MAX_DFS_STRATEGY < len(events)"""

    monkeypatch.setattr(settings, "MAX_DFS_STRATEGY", 0)

    strategy_class = StrategyFactory.get_strategy_class(events)
    assert strategy_class is IterativeSearchStrategy


def test_get_dfs_strategy(monkeypatch):
    """Tests that the StrategyFactory returns DFSSearchStrategy when
    settings.MAX_DFS_STRATEGY >= len(events)"""

    monkeypatch.setattr(settings, "MAX_DFS_STRATEGY", 1)

    strategy_class = StrategyFactory.get_strategy_class(events)
    assert strategy_class is DFSSearchStrategy
