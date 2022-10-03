from abc import ABC, abstractmethod
from typing import Tuple, Dict

from etfs.models import ETF
from pandas import read_csv, DataFrame

"""--- factory method pattern code ---"""


class ETFReader(ABC):
    """The base class for all ETF readers. Reading an ETF involves:
        1. Downloading holding data
        2. Calculating stats from holding data
        3. Entering stats into db

    Attributes:

    Methods:
        _download
        _parse_average_price_earnings
        _parse_average_ev_ebitda
    """

    def __init__(self, identifiers: Dict[str, str]):
        """Initialise an ETFReader object"""
        self._identifiers = identifiers

    def read(self) -> None:
        """The endpoint for reading an ETF and inserting the reading
        into the application database
        """
        self._download()
        self._clean_holdings()
        self._parse_average_price_earnings()
        self._parse_average_ev_ebitda()
        self._insert_reading()

    @abstractmethod
    def _download(self) -> DataFrame:
        """Download and store the data for a given ETF's holdings in a
        ``DataFrame``.

        Returns:
            A ``DataFrame`` containing holdings data for ETF being processed.
        """
        pass

    @abstractmethod
    def _clean_holdings(self) -> None:
        """Apply data-cleaning steps to the holdings ``DataFrame``, applying
        the chanes in place
        """
        pass

    @abstractmethod
    def _parse_average_price_earnings(self) -> float:
        """Parse the data contained in the holdings DataFrame to calculate
        the average price / earnings ratio for the ETF.

        Returns:
            The average price / earnings ratio for the ETF as float.

        """
        pass

    @abstractmethod
    def _parse_average_ev_ebitda(self) -> float:
        """Parse the data contained in the holdings DataFrame to calculate
        the average EV / EBITDA ratio for the ETF.

        Returns:
            The average EV / EBITDA ratio for the ETF as float.
        """
        pass

    @abstractmethod
    def _insert_reading(self) -> None:
        """Insert a reading into the application database"""
        pass


class iSharesETFReader(ETFReader):
    """The class for iShares ETF readers. Reading an ETF involves:
        1. Downloading holding data
        2. Calculating stats from holding data
        3. Entering stats into db

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
        self._holdings = read_csv(self._identifiers["holdings_url"], skiprows=[0, 1])

    def _clean_holdings(self) -> None:
        """Apply data-cleaning steps to the holdings ``DataFrame``, applying
        changes in place
        """
        self._holdings = self._holdings[self._holdings.Sector.notnull()]
        self._holdings = self._holdings[self._holdings.Sector != "Cash and/or Derivatives"]

    def _parse_average_price_earnings(self) -> float:
        """Parse the data contained in the holdings DataFrame to calculate
        the average price / earnings ratio for the ETF.

        Returns:
            The average price / earnings ratio for the ETF as float.
        """
        pass

    def _parse_average_ev_ebitda(self) -> float:
        """Parse the data contained in the holdings DataFrame to calculate
        the average EV / EBITDA ratio for the ETF.

        Returns:
            The average EV / EBITDA ratio for the ETF as float.

        """
        pass

    def _insert_reading(self) -> None:
        """Insert a reading into the application database"""
        print(self._holdings)


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
    etfs = query_etfs_by_provider(etf_provider)
    for etf_identifiers in etfs:
        creator.read(etf_identifiers)


def query_etfs_by_provider(etf_provider_name: str) -> Tuple[Dict[str, str]]:
    """Query the application database for the ETFs associated with a
    specified ETF provider

    Returns:
        A tuple containing (identifier, holdings_url) pairs
    for each ETF associated with a given ETF provider
    """
    return ETF.objects.filter(etf_issuer=etf_provider_name).values(
        "name", "holdings_url"
    )
