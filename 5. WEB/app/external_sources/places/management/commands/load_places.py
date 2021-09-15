from django.core.management.base import BaseCommand

from app.external_sources.places.services.places_importer import PlacesImporter
from app.main.settings import BASE_DIR


class Command(BaseCommand):
    help = "Load DataMicole. Example format: ./manage.py load_places places.csv "

    def add_arguments(self, parser):
        parser.add_argument("csv_name", type=str, help="Nombre del CSV")

    def handle(self, *args, **kwargs):
        csv_file = (BASE_DIR / "app/csv_files" / kwargs["csv_name"]).resolve()
        PlacesImporter(csv_file=csv_file)
