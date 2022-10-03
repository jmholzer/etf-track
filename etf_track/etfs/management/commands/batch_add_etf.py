from csv import DictReader

from django.core.management.base import BaseCommand
from etfs.models import ETF

from typing import Dict, Any

ARGS = {
    "input_file_path": {"type": str, "required": True},
}


class Command(BaseCommand):
    help = "Add all the ETFs given in a CSV file to the database"

    def add_arguments(self, parser):
        for arg in ARGS:
            parser.add_argument(
                "--" + arg, required=ARGS[arg]["required"], type=ARGS[arg]["type"]
            )

    def handle(self, *args, **options):
        self._input_file_path = options["input_file_path"]
        self._read_etfs()

    def _read_etfs(self):
        with open(self._input_file_path, "r") as input_file:
            reader = DictReader(input_file)
            for row in reader:
                # delete empty fields from row (potentially optional)
                row = {key: row[key] for key in row if row[key]}
                self._save_etf(row)

    def _save_etf(self, identifiers: Dict[str, Any]):
        _, created = ETF.objects.get_or_create(**identifiers)
        self._log_success_message(created, identifiers)

    def _log_success_message(self, created: bool, identifiers: Dict[str, Any]):
        if created:
            print(
                "Succesfully created entry for"
                f" {identifiers['name']} ({identifiers['etf_issuer']})"
            )
        else:
            print(
                f"Entry for {identifiers['name']} ({identifiers['etf_issuer']})"
                + " already in DB, no changes made"
            )
