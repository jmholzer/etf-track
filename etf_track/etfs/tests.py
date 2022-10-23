from django.test import TestCase
from pandas import DataFrame

from etfs.reader import _find_orphan_tickers


# Create your tests here.
class TestUpdateHoldings(TestCase):
    def setUp(self):
        self._downloaded_holdings = DataFrame.from_dict({
            "ticker": ["AAPL"],
            "percentage": [13.1],
        })
        self._stored_holdings = DataFrame.from_dict({
            "ticker": ["AAPL", "TSLA"],
            "percentage": [13.1, 10.2]
        })

    def test_find_orphan_tickers(self):
        result = _find_orphan_tickers(self._downloaded_holdings, self._stored_holdings)
        expected = {"TSLA"}
        self.assertEqual(result, expected)
