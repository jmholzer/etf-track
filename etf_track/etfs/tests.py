from django.test import TestCase
from pandas import DataFrame

from etfs.models import Holdings
from etfs.reader import (
    _find_orphan_tickers,
    _query_holdings_by_etf_id,
)


class TestUpdateHoldings(TestCase):
    def setUp(self):
        Holdings.objects.create(etf_id=1, ticker="AAPL", percentage=13.1)
        Holdings.objects.create(etf_id=1, ticker="TSLA", percentage=10.1)
        Holdings.objects.create(etf_id=2, ticker="NVDA", percentage=11.2)

    def test_find_orphan_tickers(self):
        downloaded_holdings = DataFrame.from_dict(
            {"ticker": ["AAPL"], "percentage": [13.1]}
        )
        stored_holdings = DataFrame.from_dict(
            {"ticker": ["AAPL", "TSLA"], "percentage": [13.1, 10.2]}
        )
        result = _find_orphan_tickers(downloaded_holdings, stored_holdings)
        expected = {"TSLA"}
        self.assertEqual(result, expected)

    def test_query_holdings_by_etf_id(self):
        expected = DataFrame.from_dict(
            {"ticker": ["AAPL", "TSLA"], "percentage": [13.1, 10.1]}
        )
        result = _query_holdings_by_etf_id(1)
        self.assertTrue(result.equals(expected))
