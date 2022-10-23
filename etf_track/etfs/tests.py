from django.test import TestCase
from pandas import DataFrame

from etfs.models import Holdings
from etfs.reader import (
    _find_orphan_tickers,
    _query_holdings_by_etf_id,
    _add_holdings,
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

    def test_add_holdings(self):
        kwargs = {
            "etf_id": 3,
            "holdings_to_add": DataFrame.from_dict(
                {"ticker": ["MSFT"], "percentage": [19.8]}
            ),
        }
        _add_holdings(**kwargs)
        result = Holdings.objects.filter(etf_id=3, ticker="MSFT", percentage=19.8).exists()
        self.assertTrue(result)
