from typing import Dict

from django.core.management.base import BaseCommand, CommandError
from etfs.models import ETF

ARG_TYPES = {"exchange": str, "ticker": str}


class Command(BaseCommand):
    help = "Run a measurement for the specified ETF"

    def add_arguments(self, parser):
        for arg in ARG_TYPES:
            parser.add_argument("--" + arg, required=True, type=ARG_TYPES[arg])

    def handle(self, *args, **options):
        identifiers = {arg: options[arg] for arg in ARG_TYPES}
        self._validate_etf(identifiers)

    def _validate_etf(self, identifiers: Dict[str, str]) -> None:
        """
        Check if the name of an ETF issuer is valid and raise an
        exception if not
        """
        if not ETF.objects.filter(
            exchange=identifiers["exchange"],
            ticker=identifiers["ticker"],
        ).exists():
            raise CommandError("ETF not found in database")
