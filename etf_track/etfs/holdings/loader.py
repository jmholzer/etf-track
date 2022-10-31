from typing import Dict, Optional, Set, Tuple

from etfs.models import ETF, Holdings
from etfs.utils import convert_queryset_to_dataframe
from pandas import DataFrame

from .reader import iSharesETFReaderCreator

ETF_PROVIDER_CREATOR_MAPPING = {"iShares": iSharesETFReaderCreator}


def read_all_etfs(etf_provider: str) -> None:
    """Reads each ETF associated with a given ETF provider"""
    creator = ETF_PROVIDER_CREATOR_MAPPING[etf_provider]()
    etfs = _query_etfs_by_provider(etf_provider)
    for etf_identifiers in etfs:
        downloaded_holdings = creator.read(etf_identifiers)
        _update_holdings(int(etf_identifiers["id"]), downloaded_holdings)


def _query_etfs_by_provider(etf_provider_name: str) -> Tuple[Dict[str, str]]:
    """Query the application database for the ETFs associated with a
    specified ETF provider

    Returns:
        A tuple containing (identifier, holdings_url) pairs
    for each ETF associated with a given ETF provider
    """
    return ETF.objects.filter(etf_issuer=etf_provider_name).values(
        "id", "name", "holdings_url"
    )


def _query_holdings_by_etf_id(etf_id: int) -> Optional[DataFrame]:
    """Query the holdings of an ETF using its id

    Arguments:
        etf_id: the id of the ETF to return holdings for

    Returns:
        a DataFrame containing the stored holdings of the given ETF, or None if
        there are no stored holdings
    """
    query_results = Holdings.objects.filter(etf_id=etf_id)
    if not query_results:
        return None
    query_results = convert_queryset_to_dataframe(query_results, exclude_id=True)
    query_results = query_results[["ticker", "percentage"]]
    return query_results


def _update_holdings(etf_id: int, downloaded_holdings: DataFrame) -> None:
    """Write the data in a 'holdings' DataFrame, obtained from an ETFReader
    object to the holdings table

    Arguments:
        downloaded_holdings: a DataFrame containing tickers and their
            percentage allocation in an ETF.
    """
    stored_holdings = _query_holdings_by_etf_id(etf_id)
    if stored_holdings is not None:
        orphan_tickers = _find_orphan_tickers(downloaded_holdings, stored_holdings)
        _delete_holdings(etf_id, orphan_tickers)
    _add_or_update_holdings(etf_id, downloaded_holdings)


def _find_orphan_tickers(
    downloaded_holdings: DataFrame, stored_holdings: DataFrame
) -> Set[str]:
    """Take a set of tickers and return a set of tickers from the holdings
    table are not present in the input ('orphan' tickers)

    Arguments:
        tickers: the set of tickers to compare against the holdings

    Returns:
        a set of orphan tickers
    """
    downloaded_tickers = set(downloaded_holdings["ticker"])
    stored_tickers = set(stored_holdings["ticker"])
    return stored_tickers - downloaded_tickers


def _add_or_update_holdings(etf_id: int, holdings_to_add: DataFrame) -> None:
    """Create or update rows in the holdings table using data in a DataFrame

    Arguments:
        etf_id: the etf id to create holdings rows for
        holdings: the DataFrame containing holdings information
    """
    for _, row in holdings_to_add.iterrows():
        Holdings.objects.update_or_create(
            etf_id=etf_id,
            ticker=row["ticker"],
            defaults={"percentage": row["percentage"]},
        )


def _delete_holdings(etf_id: int, tickers: Set[str]) -> None:
    """Delete all rows from the holdings table with the given etf_id and
    a value for ticker in the given set.

    Arguments:
        etf_id: the id of the ETF to delete holdings for
        tickers: the set of tickers to delete rows for
    """
    for ticker in tickers:
        Holdings.objects.filter(etf_id=etf_id, ticker=ticker).delete()
