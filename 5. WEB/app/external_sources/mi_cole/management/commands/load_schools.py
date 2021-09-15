from django.core.management.base import BaseCommand

from app.external_sources.mi_cole.services.school_importer import SchoolImporter
from app.main.settings import BASE_DIR


class Command(BaseCommand):
    """Load csv info to mi cole models

    Args:
        BaseCommand ([type]): [description]
    """

    help = "Load DataMicole. Example format: ./manage.py load_schools MiColePost.csv "

    def add_arguments(self, parser):
        parser.add_argument("csv_name", type=str, help="Nombre del CSV")

    def handle(self, *args, **kwargs):
        csv_file = (BASE_DIR / "app/csv_files" / kwargs["csv_name"]).resolve()
        SchoolImporter(csv_file=csv_file)
