
from kfs.settings import settings


class StrategyFactory:

    @classmethod
    def get_strategy_class(cls, events: list):
        """Determine wich strategy we use"""
        from kfs.services.strategies import (
            IterativeSearchStrategy,
            DFSSearchStrategy,
        )  # Inner import to avoid circular import
        return IterativeSearchStrategy \
            if len(events) > settings.MAX_DFS_STRATEGY \
            else DFSSearchStrategy
