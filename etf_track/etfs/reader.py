from abc import ABC, abstractmethod
from typing import List, Type

from pandas import DataFrame


class ETFReader(ABC):
    """
    The base class for all ETF readers. Reading an ETF involves:
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


class ETFReaderCreator(ABC):
    """
    The creator class for ETFReader objects.

    Attributes:

    Methods:
        factory_method
    """

    @staticmethod
    @abstractmethod
    def _factory_method(identifiers: List[str], holdings_url: str) -> Type[ETFReader]:
        """
        Returns a subclass of ETFReader.
        """
        pass

    def read(self, identifiers: List[str], holdings_url: str) -> None:
        """
        Create a reader using a factory method and use it to read
        from the specified ETF.
        """
