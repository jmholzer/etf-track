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
    """Remove rows for unused tickers from the Fundamentals table.

    Arguments:
        unused_tickers: a set containing the unused tickers to remove
    """
    for ticker in unused_tickers:
        Fundamentals.objects.filter(ticker=ticker).delete()


def _add_missing_tickers(missing_tickers: Set[str]) -> None:
    """Add rows for missing tickers to the Fundamentals table.

    Arguments:
        missing_tickers: a set containing the missing tickers to add
    """
    for ticker in missing_tickers:
        Fundamentals.objects.create(ticker=ticker)
