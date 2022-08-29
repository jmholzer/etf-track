from django.core.management.base import BaseCommand, CommandError
from etfs.measurements import iSharesETFProcessor

ETF_ISSUERS_CLASS_MAP = {
    "iShares": iSharesETFProcessor
}


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument("etf_issuers", nargs='+', type=str)

    def handle(self, *args, **options):
        for etf_issuer in options["etf_issuers"]:
            if not self._validate_etf_issuer(etf_issuer):
                raise CommandError(f"ETF issuer {etf_issuer} not recognised")
            measurer = ETF_ISSUERS_CLASS_MAP[etf_issuer]()
            measurer.process()

    def _validate_etf_issuer(self, etf_issuer: str) -> bool:
        """
        Check if the name of an ETF issuer is valid.

        Returns:
            True if the name of the ETF issuer is valid else False.
        """
        return etf_issuer in ETF_ISSUERS_CLASS_MAP
