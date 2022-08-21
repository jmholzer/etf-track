from abc import ABC, abstractmethod

from pandas import DataFrame, read_csv


class AbstractETFProcessor(ABC):
    """The base class for all ETF processors.
    'Processing' an ETF means:
        1. Downloading holding data
        2. Calculating stats from holding data
        3. Entering stats into db

    Methods:

    Attributes:

    """

    def __init__(self, identifiers, holdings_url):
        """Initialise an ETF processor object"""
        self._identifiers = identifiers
        self._holdings_url = holdings_url

    def process(self) -> None:
        """Main API entry point for processing an ETF"""
        self._holdings = self._download()
    
    def _download(self) -> DataFrame:
        """Read data from a remote CSV directly into a ``DataFrame``
        
        Returns:
            A ``DataFrame`` containing holdings data for ETF being processed.
        """
        return read_csv(self._holdings_url)

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


class iSharesETFProcessor(AbstractETFProcessor):
    """Class for processing ETFs marketed by iShares (ishares.com)

    Methods:

    Attributes:

    """

    def _download(self):
        pass
