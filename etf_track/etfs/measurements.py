from abc import ABC, abstractmethod
from datetime import datetime

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

    @abstractmethod
    def _download(self) -> DataFrame:
        """Download and store the data for a given ETF's holdings in a
        ``DataFrame``.

        Returns:
            A ``DataFrame`` containing holdings data for ETF being processed.
        """
        pass

    def _get_measurement_datetime(self) -> datetime:
        """

        Returns:
            A datetime object containing the date / time of measurement.

        """
        return datetime.now()

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
        """Read data from a remote CSV directly into a ``DataFrame``

        Returns:
            A ``DataFrame`` containing holdings data for ETF being processed.
        """
        return read_csv(self._holdings_url)

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
