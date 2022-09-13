from abc import ABC, abstractmethod
from typing import List, Tuple

from pandas import DataFrame

from models import ETF

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

    def __init__(self, identifiers: List[str], holdings_url: str):
        """Initialise an ETFReader object"""
        self._identifiers = identifiers
        self._holdings_url = holdings_url

    def read(self) -> None:
        """The endpoint for reading an ETF and inserting the reading
        into the application database
        """
        self._download()
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
        """Insert a reading into the application database
        """
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
        pass

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
        """Insert a reading into the application database
        """
        pass


class ETFReaderCreator(ABC):
    """The creator class for ETFReader objects.

    Attributes:

    Methods:
        _factory_method
        read
    """

    @staticmethod
    @abstractmethod
    def _factory_method(identifiers: List[str], holdings_url: str) -> ETFReader:
        """Returns a subclass of ETFReader.
        """
        pass

    def read(self, identifiers: List[str], holdings_url: str) -> None:
        """Create a reader using a factory method and use it to read
        from the specified ETF.
        """
        reader = self._factory_method(identifiers, holdings_url)
        reader.read()


class iSharesETFReaderCreator(ETFReaderCreator):
    """The creator class for iSharesETFReader objects

    Attributes:

    Methods:
        _factory_method
        read
    """

    @staticmethod
    def _factory_method(identifiers: List[str], holdings_url: str) -> ETFReader:
        """Returns a subclass of ETFReader.
        """
        return iSharesETFReader(identifiers, holdings_url)


"""--- client code ---"""


def read_all_etfs(etf_provider_name: str) -> None:
    """Reads each ETF associated with a given ETF provider
    """
    reader_factory = get_etf_reader_factory(etf_provider_name)
    ETFs = query_etfs_by_provider(etf_provider_name)
    for identifiers, holdings_url in ETFs:
        reader_factory.read(identifiers, holdings_url)


def get_etf_reader_factory(etf_provider_name: str) -> ETFReaderCreator:
    """Create an ETFReader factory given the name of the ETF provider

    Returns:
        An ETFReader factory for the given etf_provider
    """
    etf_provider_product_mapping = {
        "iShares": iSharesETFReaderCreator
    }
    return etf_provider_product_mapping[etf_provider_name]()


def query_etfs_by_provider(etf_provider_name: str) -> Tuple[Tuple[List[str], str]]:
    """Query the application database for the ETFs associated with a
    specified ETF provider

    Returns:
        A tuple containing (identifier, holdings_url) pairs
    for each ETF associated with a given ETF provider
    """
    pass
