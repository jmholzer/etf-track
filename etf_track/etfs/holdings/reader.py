from abc import ABC, abstractmethod
from typing import Dict

from pandas import DataFrame, read_csv


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
        holdings = self._clean_holdings(holdings)
        holdings = self._transform_holdings(holdings)
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
    def _clean_holdings(self, holdings: DataFrame) -> DataFrame:
        """Apply data-cleaning steps to the holdings ``DataFrame``"""
        pass

    @abstractmethod
    def _transform_holdings(self, holdings: DataFrame) -> DataFrame:
        """Transform the dataframe so that it contains two columns, ticker
        and percentage of fund
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

    def _clean_holdings(self, holdings) -> DataFrame:
        """Apply data-cleaning steps to the holdings ``DataFrame``"""
        holdings = holdings[holdings.Sector.notnull()]
        holdings = holdings[holdings.Sector != "Cash and/or Derivatives"]
        return holdings

    def _transform_holdings(self, holdings: DataFrame) -> DataFrame:
        """Transform the dataframe so that it contains two columns, ticker
        and percentage of fund
        """
        holdings = holdings[["Ticker", "Weight (%)"]]
        holdings = holdings.rename(
            columns={"Ticker": "ticker", "Weight (%)": "percentage"}
        )
        return holdings


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
