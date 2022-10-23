from abc import ABC, abstractmethod
from typing import Dict, Set, Tuple

from pandas import DataFrame, read_csv

from etfs.models import ETF, Holdings
from etfs.utils import convert_queryset_to_dataframe

"""--- factory method pattern code ---"""


class ETFReader(ABC):
    """The base class for all ETF readers. ETF reader objects download, clean
    and expose an ETF's holdings data as a DataFrame.

    Attributes:
        _identifiers

    Methods:
        _download
    """

    def __init__(self, identifiers: Dict[str, str]):
        """Initialise an ETFReader object"""
        self._identifiers = identifiers

    def read(self) -> DataFrame:
        """The endpoint for reading an ETF's holdings and returning
        them in a ``DataFrame``

        Returns:
            A ``DataFrame`` containing the ticker, exchange and weight of
            the holdings of the ETF
        """
        holdings = self._download()
        self._clean_holdings(holdings)
        self._transform_holdings(holdings)
        return holdings

    @abstractmethod
    def _download(self) -> DataFrame:
        """Download and store the data for a given ETF's holdings in a
        ``DataFrame``.

        Returns:
            A ``DataFrame`` containing holdings data for ETF being processed.
        """
        pass

    @abstractmethod
    def _clean_holdings(self, holdings: DataFrame) -> None:
        """Apply data-cleaning steps to the holdings ``DataFrame``, applying
        the chanes in place
        """
        pass

    @abstractmethod
    def _transform_holdings(self, holdings: DataFrame) -> None:
        """Transform the dataframe so that it contains two columns, ticker
        and percentage of fund, applying changes in-place
        """
        pass


class iSharesETFReader(ETFReader):
    """The class for iShares ETF readers.

    Attributes:

    Methods:
        _download
        _parse_average_price_earnings
        _parse_average_ev_ebitda
    """

    def _download(self) -> DataFrame:
        """Download and store the data for a given ETF's holdings in a
        ``DataFrame``.

        Returns:
            A ``DataFrame`` containing holdings data for ETF being processed.
        """
        return read_csv(self._identifiers["holdings_url"], skiprows=[0, 1])

    def _clean_holdings(self, holdings) -> None:
        """Apply data-cleaning steps to the holdings ``DataFrame``, applying
        changes in-place
        """
        holdings = holdings[holdings.Sector.notnull()]
        holdings = holdings[holdings.Sector != "Cash and/or Derivatives"]

    def _transform_holdings(self, holdings: DataFrame) -> None:
        """Transform the dataframe so that it contains two columns, ticker
        and percentage of fund, applying changes in-place
        """
        holdings = holdings[["Ticker", "Weight (%)"]]
        holdings = holdings.rename(columns={"Ticker": "ticker", "Weight (%)": "weight"})


class ETFReaderCreator(ABC):
    """The creator class for ETFReader objects.

    Attributes:

    Methods:
        _factory_method
        read
    """

    @staticmethod
    @abstractmethod
    def _factory_method(identifiers: Dict[str, str]) -> ETFReader:
        """Returns a subclass of ETFReader."""
        pass

    def read(self, identifiers: Dict[str, str]) -> DataFrame:
        """Create a reader using a factory method and use it to read
        from the specified ETF.
        """
        reader = self._factory_method(identifiers)
        return reader.read()


class iSharesETFReaderCreator(ETFReaderCreator):
    """The creator class for iSharesETFReader objects

    Attributes:

    Methods:
        _factory_method
        read
    """

    @staticmethod
    def _factory_method(identifiers: Dict[str, str]) -> ETFReader:
        """Returns a subclass of ETFReader."""
        return iSharesETFReader(identifiers)


"""--- client code ---"""

ETF_PROVIDER_CREATOR_MAPPING = {"iShares": iSharesETFReaderCreator}


def read_all_etfs(etf_provider: str) -> None:
    """Reads each ETF associated with a given ETF provider"""
    creator = ETF_PROVIDER_CREATOR_MAPPING[etf_provider]()
    etfs = _query_etfs_by_provider(etf_provider)
    for etf_identifiers in etfs:
        downloaded_holdings = creator.read(etf_identifiers)
        _update_holdings(etf_identifiers["etf_id"], downloaded_holdings)


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


def _query_holdings_by_etf_id(etf_id: int) -> DataFrame:
    """Query the holdings of an ETF using its id

    Arguments:
        etf_id: the id of the ETF to return holdings for

    Returns:
        a DataFrame containing the stored holdings of the given ETF
    """
    query_results = Holdings.objects.filter(etf_id=etf_id)
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
            defaults={"percentage": row["percentage"]}
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
