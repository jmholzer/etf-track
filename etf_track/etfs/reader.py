from abc import ABC, abstractmethod
from typing import Tuple, Dict

from etfs.models import ETF
from pandas import read_csv, DataFrame

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
        changes in place
        """
        holdings = holdings[holdings.Sector.notnull()]
        holdings = holdings[holdings.Sector != "Cash and/or Derivatives"]


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

    def read(self, identifiers: Dict[str, str]) -> None:
        """Create a reader using a factory method and use it to read
        from the specified ETF.
        """
        reader = self._factory_method(identifiers)
        reader.read()


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

ETF_PROVIDER_CREATOR_MAPPING = {
    "iShares": iSharesETFReaderCreator
}


def read_all_etfs(etf_provider: str) -> None:
    """Reads each ETF associated with a given ETF provider"""
    creator = ETF_PROVIDER_CREATOR_MAPPING[etf_provider]()
    etfs = _query_etfs_by_provider(etf_provider)
    for etf_identifiers in etfs:
        creator.read(etf_identifiers)


def _write_holdings(holdings: DataFrame) -> None:
    """Write the data in a 'holdings' DataFrame, obtained from an ETFReader
    object to the holdings table"""
    pass


def _query_etfs_by_provider(etf_provider_name: str) -> Tuple[Dict[str, str]]:
    """Query the application database for the ETFs associated with a
    specified ETF provider

    Returns:
        A tuple containing (identifier, holdings_url) pairs
    for each ETF associated with a given ETF provider
    """
    return ETF.objects.filter(etf_issuer=etf_provider_name).values(
        "name", "holdings_url"
    )
