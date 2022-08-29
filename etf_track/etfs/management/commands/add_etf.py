from django.core.management.base import BaseCommand, CommandError
from etfs.models import ETF


ARG_TYPES = {
    "exchange": str,
    "ticker": str,
    "name": str
}


class Command(BaseCommand):
    help = "Add an ETF to the database"

    def add_arguments(self, parser):
        for arg in ARG_TYPES:
            parser.add_argument("--" + arg, required=True, type=ARG_TYPES[arg])

    def handle(self, *args, **options):
        identifiers = {}
        for arg in ARG_TYPES:
            identifiers[arg] = options[arg]
        self._save_etf(identifiers)
        
    def _save_etf(self, identifiers):
        etf = ETF(
            name=identifiers["name"],
            ticker=identifiers["ticker"],
            exchange=identifiers["exchange"]
        )
        etf.save()
