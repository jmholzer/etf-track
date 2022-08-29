from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Add an ETF to the database"

    def add_arguments(self, parser):
        parser.add_argument("identifiers", nargs="+", type=str)

    def handle(self, *args, **options):
        pass
