from django.core.management.base import BaseCommand
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
        _, created = ETF.objects.get_or_create(
            name=identifiers["name"],
            ticker=identifiers["ticker"],
            exchange=identifiers["exchange"]
        )
        self._log_success_message(created)

    def _log_success_message(self, created):
        if created:
            print("Succesfully created")
        else:
            print("Object already in DB, no changes made")
