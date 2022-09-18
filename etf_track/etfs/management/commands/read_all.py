from django.core.management.base import BaseCommand, CommandError
from etfs.models import ETF
from etfs.reader import read_all_etfs


class Command(BaseCommand):
    help = "Run a measurement for the specified ETF"

    def add_arguments(self, parser):
        parser.add_argument("--" + "etf_issuer", required=True, type=str)

    def handle(self, *args, **options):
        etf_issuer = options["etf_issuer"]
        self._validate_etf(etf_issuer)
        read_all_etfs(etf_issuer)

    def _validate_etf(self, etf_issuer: str) -> None:
        """Check if the name of an ETF issuer is valid and raise an
        exception if not
        """
        if not ETF.objects.filter(etf_issuer=etf_issuer).exists():
            raise CommandError("ETF not found in database")
