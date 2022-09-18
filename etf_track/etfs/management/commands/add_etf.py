from django.core.management.base import BaseCommand
from etfs.models import ETF


ARGS = {
    "etf_issuer": {"type": str, "required": True},
    "ticker": {"type": str, "required": True},
    "exchange": {"type": str, "required": True},
    "name": {"type": str, "required": True},
    "holdings_url": {"type": str, "required": True},
    "sector": {"type": str, "required": False},
}


class Command(BaseCommand):
    help = "Add an ETF to the database"

    def add_arguments(self, parser):
        for arg in ARGS:
            parser.add_argument(
                "--" + arg, required=ARGS[arg]["required"], type=ARGS[arg]["type"]
            )

    def handle(self, *args, **options):
        identifiers = {}
        for arg in ARGS:
            identifiers[arg] = options[arg]
        self._save_etf(identifiers)

    def _save_etf(self, identifiers):
        _, created = ETF.objects.get_or_create(**identifiers)
        self._log_success_message(created)

    def _log_success_message(self, created):
        if created:
            print("Succesfully created")
        else:
            print("Object already in DB, no changes made")
