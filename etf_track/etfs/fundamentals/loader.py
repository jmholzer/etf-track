from typing import Set

from etfs.models import Fundamentals, Holdings


def update_fundamentals() -> None:
    """Update the Fundamentals table by comparing tickers with
    the Holdings table.
    """
    pass


def _read_all_holding_tickers() -> Set[str]:
    """Read all the tickers in the Holdings table

    Returns:
        A set of all the tickers in the Holdings table
    """
    return {row["ticker"] for row in Holdings.objects.values("ticker")}


def _read_all_fundamentals_tickers() -> Set[str]:
    """Read all the tickers in the Holdings table

    Returns:
        A set of all the tickers in the Holdings table
    """
    return {row["ticker"] for row in Fundamentals.objects.values("ticker")}


def _remove_unused_tickers(unused_tickers: Set[str]) -> None:
    """Remove unused tickers from the Fundamentals table.

    Arguments:
        unused_tickers: a set containing the unused tickers to remove
    """
    pass


def _add_missing_tickers(missing_tickers: Set[str]) -> None:
    """Add missing tickers to the Fundamentals table.

    Arguments:
        missing_tickers: a set containing the missing tickers to add
    """
    pass
